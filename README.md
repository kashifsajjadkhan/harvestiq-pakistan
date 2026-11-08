# HarvestIQ Pakistan <img width="64" height="66" alt="HarvestIQ logo" src="https://github.com/user-attachments/assets/b4cf8190-f4ec-4e3f-a62d-9c1934ce4370" />

**Pakistan's first integrated pre & post-harvest loss intelligence platform** — satellite crop-health monitoring before harvest, and a risk calculator for what happens after.

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://kashifsajjadkhan.github.io/harvestiq-pakistan/)
![Sentinel-2](https://img.shields.io/badge/NDVI-Sentinel--2%20L2A%2010m-blue)
![Districts](https://img.shields.io/badge/districts-16-orange)
![PWA](https://img.shields.io/badge/PWA-offline--capable-informational)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)

🔗 **Live app:** [kashifsajjadkhan.github.io/harvestiq-pakistan](https://kashifsajjadkhan.github.io/harvestiq-pakistan/)

🎬 **Demo video:** [demo.mp4](https://github.com/kashifsajjadkhan/harvestiq-pakistan/raw/main/demo.mp4)

---

## The problem

Pakistan loses an estimated **35–40% of its fruit and vegetable harvest after it leaves the field** — worth over **PKR 345 billion** every year. Smallholder farmers, who grow most of the country's produce, make harvest and storage decisions with no data: no sense of crop condition, no estimate of spoilage risk, no sense of what a day's delay costs them in rupees.

## What this does

HarvestIQ is a bilingual (English/Urdu), offline-capable web app that walks a farmer through three steps:

1. **Satellite crop-health check** — pick a district and a crop. The app shows the real Sentinel-2 NDVI picture for that district, the NDVI number, the scene date and a short note on the vegetation. The crop sets the interpretation: each of the 12 crops (mango, citrus, guava, tomato, potato and more) has its own healthy-NDVI threshold. The NDVI also feeds the post-harvest risk score.
2. **Post-harvest risk model** — the farmer enters harvest conditions (days since harvest, maturity, harvest method, storage, packaging, temperature, humidity, transport) and gets a nine-factor spoilage-risk score, estimated shelf life remaining, and a prioritized action list.
3. **Economic calculator** — quantity and market price in → estimated loss in PKR, potential savings from the recommended actions, and the break-even price needed to cover losses.

## Live satellite data

Crop-health readings come from **Sentinel-2 L2A (10 m resolution)** via the **Copernicus Data Space** (STAC and Process APIs). Punjab's smallholder plots are smaller than a single MODIS pixel (250 m), so MODIS could not resolve the farms this tool is for — Sentinel-2 can.

How the pipeline works:

- **`.github/workflows/sentinel-refresh.yml`** runs every Monday (03:00 UTC) and on demand
- **`scripts/fetch_sentinel.py`** fetches the latest clear scene per district and writes **`data/sentinel-ndvi.json`** plus one real NDVI picture per district in **`data/ndvi-pics/`**
- Cloud masking uses the SCL band (vegetation and bare soil only), with a **20% clear-pixel quality gate** and a **30-day lookback**; if no clear scene exists, the previous value is kept rather than invented
- Values are ~2 km samples around each district centre, labelled by district name, for all **16 districts**
- The app loads the snapshot from its own domain (no CORS issues, works offline once cached); if the snapshot is ever missing it falls back to a clearly-labelled modelled estimate

The previous MODIS pipeline (`scripts/fetch_ndvi.py`, `.github/workflows/ndvi-refresh.yml`) is retained for manual runs only; its weekly schedule is disabled.

## Field validation

The satellite numbers are checked against the ground. Field photos with GPS, taken in **Bhakkar, Punjab**, are compared against the Sentinel-2 NDVI for the same places and dates. The full record — ground photos, satellite pictures, Google Maps views, NDVI values and verdicts — is on the **[field validation page](https://kashifsajjadkhan.github.io/harvestiq-pakistan/validation.html)**. Current coverage: four ground checks across three of the tool's crops (citrus, mango, guava), with more points being added as fieldwork continues.

## Project structure

```
├── index.html                  # the entire app (single file)
├── validation.html             # field validation — ground truth vs satellite
├── validation/                 # validation photos, satellite pictures, maps
├── data/sentinel-ndvi.json     # weekly Sentinel-2 NDVI snapshot (auto-generated)
├── data/ndvi-pics/             # real per-district NDVI pictures (auto-generated)
├── scripts/fetch_sentinel.py   # Sentinel-2 snapshot + picture pipeline
├── scripts/fetch_ndvi.py       # original MODIS fetcher (manual use only)
├── .github/workflows/          # weekly refresh automation
├── manifest.json / sw.js        # PWA install + offline support
├── panda-globe.gif             # hero artwork
├── sentinel-mascot.gif         # upgrade-note mascot
├── satellite.png               # artwork (unused)
└── demo.mp4                    # promo video
```

## Run it locally

No build step — it is a static site:

```bash
git clone https://github.com/kashifsajjadkhan/harvestiq-pakistan.git
cd harvestiq-pakistan
python3 -m http.server 8000
# open http://localhost:8000
```

To refresh the satellite snapshot manually, set your Copernicus Data Space credentials and run:

```bash
export COPERNICUS_USERNAME="you@example.com"
export COPERNICUS_PASSWORD="your-password"
python3 scripts/fetch_sentinel.py
```

## Data sources & methodology

- **Vegetation data:** Sentinel-2 L2A via the Copernicus Data Space. Sentinel data is free, full and open under EU law (Regulation (EU) No 377/2014); public use requires the credit line **"Contains modified Copernicus Sentinel data 2026"**, shown on the app and the validation page.
- **Risk model** informed by CAAS (Chinese Academy of Agricultural Sciences) post-harvest training material and FAO post-harvest loss studies for South Asian supply chains (Ahmad et al. 2021; ADB 2019), as cited in the app
- NDVI health thresholds are calibrated per crop; the app labels every reading with its source and acquisition date. NDVI measures vegetation greenness — the app does not claim it measures maturity or harvest readiness directly.

## Roadmap

- Real soil-moisture index (NDMI, from Sentinel-2 SWIR band B11)
- True district averages from boundary polygons, then cropland-only masking
- Per-district NDVI time series
- District-level push alerts (SMS/WhatsApp) for high-risk harvest windows
- On-device NDVI from drone imagery for individual fields
- Market-price feeds for the economic calculator

## Author

**Kashif Sajjad Khan** — [GitHub](https://github.com/kashifsajjadkhan) · Kashifsajjad7172@gmail.com

Built for agricultural extension officers and smallholder farmers in Pakistan. Open to collaboration, especially on applied remote sensing for agriculture.

## License

CC BY-NC 4.0 — see [LICENSE](LICENSE).
