#!/usr/bin/env python3
"""Weekly MODIS NDVI snapshot for HarvestIQ Pakistan.

Fetches the latest MOD13Q1 16-day NDVI composite for each district from the
NASA ORNL DAAC subset API (server-side: no CORS issues) and writes
data/ndvi.json, which the site loads from its own domain.

Safety: entries that fail to refresh keep their previous values — good data
is never clobbered by a bad run.
"""
import json
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

API = "https://modis.ornl.gov/rst/api/v1/MOD13Q1/subset"
BAND = "250m_16_days_NDVI"
SCALE = 0.0001
FILL = -2000

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

OUT = Path(__file__).resolve().parent.parent / "data" / "ndvi.json"


def doy(d: date) -> str:
    return f"A{d.year}{d.timetuple().tm_yday:03d}"


def fetch_district(name: str, lat: float, lon: float) -> dict:
    end = date.today() - timedelta(days=8)    # allow for composite publication lag
    start = date.today() - timedelta(days=80)
    url = (
        f"{API}?latitude={lat}&longitude={lon}"
        f"&startDate={doy(start)}&endDate={doy(end)}"
        f"&band={BAND}&kmAboveBelow=1&kmLeftRight=1"
    )
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": "HarvestIQ-Pakistan/1.0"}
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.load(resp)

    rows = [r for r in data.get("subset", []) if r.get("band") == BAND]
    if not rows:
        raise RuntimeError("no NDVI band in response")
    nrows, ncols = data["nrows"], data["ncols"]
    center = (nrows // 2) * ncols + (ncols // 2)

    latest_idx = next(
        (i for i in range(len(rows) - 1, -1, -1) if rows[i]["data"][center] > FILL),
        None,
    )
    if latest_idx is None:
        raise RuntimeError("no valid composite in window")
    latest = rows[latest_idx]
    prev = rows[latest_idx - 1] if latest_idx > 0 else latest

    grid = [None if v <= FILL else round(v * SCALE, 4) for v in latest["data"]]
    return {
        "name": name,
        "lat": lat,
        "lon": lon,
        "ndvi": round(latest["data"][center] * SCALE, 4),
        "prev_ndvi": round(prev["data"][center] * SCALE, 4),
        "date": latest["calendar_date"][:10],
        "rows": nrows,
        "cols": ncols,
        "grid": grid,
    }


def main() -> int:
    previous = {}
    if OUT.exists():
        try:
            previous = {d["name"]: d for d in json.loads(OUT.read_text())["districts"]}
        except Exception as e:
            print(f"warning: could not read existing snapshot: {e}", file=sys.stderr)

    districts_out = []
    failures = []
    for name, lat, lon in DISTRICTS:
        try:
            districts_out.append(fetch_district(name, lat, lon))
            print(f"ok   {name}")
        except Exception as e:
            failures.append(name)
            print(f"fail {name}: {e}", file=sys.stderr)
            if name in previous:
                districts_out.append(previous[name])
                print(f"kept previous values for {name}")

    if not districts_out:
        print("error: no district data available, not writing file", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(
        {
            "updated_at": date.today().isoformat(),
            "product": "MOD13Q1",
            "source": "NASA ORNL DAAC",
            "districts": districts_out,
        },
        indent=1,
    ))
    print(f"wrote {OUT} ({len(districts_out)} districts, {len(failures)} failures)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
