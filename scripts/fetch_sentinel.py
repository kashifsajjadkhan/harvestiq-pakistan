"""
Sentinel-2 NDVI fetch for HarvestIQ (parallel test pipeline).

Method (see repo docs for the full explanation):
  1. Authenticate to Copernicus Data Space (password grant, token fresh each run).
  2. For each district, list recent Sentinel-2 L2A scenes via the STAC catalog.
  3. For each candidate scene (newest first), request a small raster (B04, B08, SCL)
     from the Sentinel Hub Process API and compute NDVI locally:
       - keep only clear land pixels: SCL == 4 (vegetation) or 5 (bare soil)
       - NDVI = (B08 - B04) / (B08 + B04)
       - accept the scene only if >= MIN_CLEAR_FRACTION of pixels are clear
  4. If no scene passes, keep the previous value (never publish a cloudy number).
  5. Write data/sentinel-ndvi.json (test file; the live MODIS snapshot is untouched).

Credentials come only from the environment (GitHub Actions secrets):
  COPERNICUS_USERNAME, COPERNICUS_PASSWORD
"""

import json
import math
import os
import sys
from datetime import datetime, timedelta, timezone

import numpy as np
import requests
from tifffile import imread

IDENTITY_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"
PROCESS_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"

# Districts: identical to the MODIS pipeline (scripts/fetch_ndvi.py) so the
# Sentinel-2 numbers are directly comparable with the live snapshot.
DISTRICTS = [
    ("Lahore", 31.55, 74.35),
    ("Multan", 30.20, 71.47),
    ("Faisalabad", 31.42, 73.08),
    ("Bahawalpur", 29.40, 71.68),
    ("Rahim Yar Khan", 28.42, 70.30),
    ("Gujranwala", 32.15, 74.18),
    ("Sialkot", 32.50, 74.53),
    ("Sargodha", 32.08, 72.67),
    ("Karachi", 24.86, 67.01),
    ("Hyderabad", 25.40, 68.37),
    ("Sukkur", 27.70, 68.86),
    ("Larkana", 27.56, 68.22),
    ("Peshawar", 34.01, 71.57),
    ("Swat", 35.22, 72.42),
    ("Quetta", 30.19, 67.00),
    ("Turbat", 25.99, 63.05),
]

HALF_BOX_DEG = 0.01      # ~1.9 x 2.2 km box around the district centre
LOOKBACK_DAYS = 30
MAX_CANDIDATES = 8        # newest scenes to try per district
MIN_CLEAR_FRACTION = 0.20 # reject scenes with fewer clear pixels
OUTPUT_PATH = "data/sentinel-ndvi.json"

EVALSCRIPT = """//VERSION=3
function setup() {
  return {
    input: [{bands: ["B04", "B08", "SCL"]}],
    // FLOAT32: B04/B08 arrive as 0-1 reflectance decimals, which UINT16
    // output would truncate to 0/1. NDVI is scale-invariant, so decimals
    // work fine; SCL classes (4, 5, ...) survive as exact floats.
    output: {bands: 3, sampleType: "FLOAT32"}
  };
}
function evaluatePixel(sample) {
  return [sample.B04, sample.B08, sample.SCL];
}
"""


def get_token(username, password):
    resp = requests.post(
        IDENTITY_URL,
        data={
            "grant_type": "password",
            "client_id": "cdse-public",
            "username": username,
            "password": password,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def candidate_scenes(token, lon, lat, start, end):
    """Recent Sentinel-2 L2A scenes over the point, newest first."""
    resp = requests.post(
        STAC_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "collections": ["sentinel-2-l2a"],
            "bbox": [lon - HALF_BOX_DEG, lat - HALF_BOX_DEG,
                     lon + HALF_BOX_DEG, lat + HALF_BOX_DEG],
            "datetime": f"{start.isoformat()}/{end.isoformat()}",
            "limit": 50,
            "sortby": [{"field": "properties.datetime", "direction": "desc"}],
        },
        timeout=60,
    )
    resp.raise_for_status()
    scenes = []
    seen_dates = set()
    for feat in resp.json().get("features", []):
        dt = feat["properties"]["datetime"][:10]
        if dt in seen_dates:
            continue
        seen_dates.add(dt)
        scenes.append({
            "date": dt,
            "cloud_cover": feat["properties"].get("eo:cloud_cover"),
        })
    return scenes[:MAX_CANDIDATES]


def scene_ndvi(token, lon, lat, date):
    """Fetch one day's raster and compute masked mean NDVI + clear fraction."""
    min_lon, max_lon = lon - HALF_BOX_DEG, lon + HALF_BOX_DEG
    min_lat, max_lat = lat - HALF_BOX_DEG, lat + HALF_BOX_DEG
    width = max(10, round((max_lon - min_lon) * 111320 * math.cos(math.radians(lat)) / 10))
    height = max(10, round((max_lat - min_lat) * 110540 / 10))
    day_start = f"{date}T00:00:00Z"
    day_end = f"{date}T23:59:59Z"
    resp = requests.post(
        PROCESS_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "input": {
                "bounds": {
                    "bbox": [min_lon, min_lat, max_lon, max_lat],
                    "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"},
                },
                "data": [{"type": "sentinel-2-l2a",
                          "dataFilter": {"timeRange": {"from": day_start, "to": day_end}}}],
            },
            "output": {
                "width": width,
                "height": height,
                "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}],
            },
            "evalscript": EVALSCRIPT,
        },
        timeout=120,
    )
    resp.raise_for_status()
    arr = imread(__import__("io").BytesIO(resp.content))
    # tifffile returns (height, width, bands) for interleaved TIFFs and
    # (bands, height, width) for planar TIFFs; normalize to (bands, H, W).
    if arr.ndim == 3 and arr.shape[2] == 3 and arr.shape[0] != 3:
        arr = np.moveaxis(arr, -1, 0)
    if arr.ndim == 3:
        red, nir, scl = arr[0].astype(np.float64), arr[1].astype(np.float64), arr[2]
    else:  # single band fallback (should not happen with 3-band evalscript)
        raise ValueError(f"unexpected raster shape {arr.shape}")
    # DEBUG: reveal exactly what the raster contains (removed after validation)
    uniq, counts = np.unique(scl, return_counts=True)
    top = sorted(zip(counts.tolist(), uniq.tolist()), reverse=True)[:8]
    print(f"DEBUG raster shape={arr.shape} dtype={arr.dtype} "
          f"red range=({red.min():.0f},{red.max():.0f}) "
          f"nir range=({nir.min():.0f},{nir.max():.0f}) "
          f"scl top values(count)= {top}")
    valid = ((scl == 4) | (scl == 5)) & ((nir + red) > 0)
    clear_fraction = float(valid.sum() / valid.size) if valid.size else 0.0
    if valid.sum() == 0:
        return None, clear_fraction
    ndvi = ((nir - red) / (nir + red))[valid]
    return float(ndvi.mean()), clear_fraction


def main():
    username = os.environ.get("COPERNICUS_USERNAME")
    password = os.environ.get("COPERNICUS_PASSWORD")
    if not username or not password:
        print("ERROR: COPERNICUS_USERNAME / COPERNICUS_PASSWORD not set", file=sys.stderr)
        sys.exit(1)

    token = get_token(username, password)
    print("authenticated to Copernicus Data Space")

    now = datetime.now(timezone.utc)
    start = now - timedelta(days=LOOKBACK_DAYS)

    previous = {}
    if os.path.exists(OUTPUT_PATH):
        try:
            previous = {d["name"]: d for d in json.load(open(OUTPUT_PATH))["districts"]}
        except Exception:
            previous = {}

    results = []
    for name, lat, lon in DISTRICTS:
        try:
            scenes = candidate_scenes(token, lon, lat, start, now)
        except Exception as exc:
            print(f"{name}: catalog search failed ({exc}); keeping previous")
            scenes = []
        accepted = None
        for scene in scenes:
            try:
                ndvi, clear = scene_ndvi(token, lon, lat, scene["date"])
            except Exception as exc:
                print(f"{name}: {scene['date']} raster failed ({exc})")
                continue
            print(f"{name}: {scene['date']} clear={clear:.2f} ndvi={ndvi}")
            if ndvi is not None and clear >= MIN_CLEAR_FRACTION:
                accepted = {"date": scene["date"], "ndvi": round(ndvi, 4),
                            "clear_fraction": round(clear, 3)}
                break
        if accepted is None:
            prev = previous.get(name)
            if prev:
                print(f"{name}: no clear scene; keeping previous {prev['ndvi']} ({prev['date']})")
                results.append(prev)
            else:
                print(f"{name}: no clear scene and no previous value; skipped")
            continue
        prev = previous.get(name)
        entry = {
            "name": name, "lat": lat, "lon": lon,
            "ndvi": accepted["ndvi"],
            "prev_ndvi": prev["ndvi"] if prev else None,
            "date": accepted["date"],
            "clear_fraction": accepted["clear_fraction"],
        }
        results.append(entry)

    out = {
        "updated_at": now.strftime("%Y-%m-%d"),
        "product": "S2MSI2A",
        "source": "Copernicus Data Space (Sentinel-2 L2A)",
        "method": "SCL-masked mean NDVI (SCL 4/5 only), >=20% clear pixels, 30-day lookback",
        "districts": results,
    }
    os.makedirs("data", exist_ok=True)
    json.dump(out, open(OUTPUT_PATH, "w"), indent=2)
    print(f"wrote {OUTPUT_PATH} with {len(results)} districts")


if __name__ == "__main__":
    main()
