# HarvestIQ Pakistan <img width="64" height="66" alt="image" src="https://github.com/user-attachments/assets/b4cf8190-f4ec-4e3f-a62d-9c1934ce4370" />


**Field-to-market intelligence for Pakistani smallholder farmers** — satellite crop-health monitoring before harvest, and a post-harvest loss calculator for what happens after.

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://kashifsajjadkhan.github.io/harvestiq-pakistan/)
![NDVI](https://img.shields.io/badge/NDVI-NASA%20MODIS%20MOD13Q1-blue)
![Districts](https://img.shields.io/badge/districts-16-orange)
![PWA](https://img.shields.io/badge/PWA-offline--capable-informational)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)

🔗 **Live app:** [kashifsajjadkhan.github.io/harvestiq-pakistan](https://kashifsajjadkhan.github.io/harvestiq-pakistan/)

https://github.com/kashifsajjadkhan/harvestiq-pakistan/raw/main/demo.mp4

---

## The problem

Pakistan loses an estimated **35–40% of its fruit and vegetable harvest after it leaves the field** — worth over **PKR 345 billion** every year. Smallholder farmers, who grow most of the country's produce, make harvest and storage decisions with no data: no sense of crop readiness, no estimate of spoilage risk, no sense of what a day's delay costs them in rupees.

## What this does

HarvestIQ is a bilingual (English/Urdu), offline-capable web app that walks a farmer through three steps:

1. **Satellite crop-health check** — pick a district and crop; the app pulls the latest NASA MODIS NDVI reading for that district, shows the trend against the previous 16-day period, and gives a harvest-readiness verdict (Optimal / Moderate / Stressed).
2. **Post-harvest risk model** — the farmer enters harvest conditions (days since harvest, maturity, harvest method, storage, packaging, temperature, humidity, transport) and gets a spoilage-risk score, estimated shelf life remaining, and a prioritized action list.
3. **Economic calculator** — quantity and market price in → estimated loss in PKR, potential savings from recommended actions, and the break-even price needed to cover losses.

## Live satellite data

Crop-health readings come from the **NASA MODIS Terra MOD13Q1 product** (16-day NDVI composite, 250 m resolution) via the ORNL DAAC subset API, sampled over a ~2 km box around each of the 16 covered districts.

To keep the app fast and independent of live API availability, a scheduled pipeline refreshes the data automatically:

- **`.github/workflows/ndvi-refresh.yml`** runs every Monday and on demand
- **`scripts/fetch_ndvi.py`** fetches the latest composite per district and writes **`data/ndvi.json`**
- The app loads the snapshot from its own domain (no CORS issues, works offline once cached); if the snapshot is ever missing it falls back to a direct API call, then to a clearly-labelled modelled estimate

## Project structure

```
├── index.html                  # the entire app (single file)
├── data/ndvi.json              # weekly MODIS NDVI snapshot (auto-generated)
├── scripts/fetch_ndvi.py       # snapshot fetch script
├── .github/workflows/          # weekly refresh automation
├── manifest.json / sw.js        # PWA install + offline support
├── satellite.png               # artwork
└── demo.mp4                    # promo video
```

## Run it locally

No build step — it's a static site:

```bash
git clone https://github.com/kashifsajjadkhan/harvestiq-pakistan.git
cd harvestiq-pakistan
python3 -m http.server 8000
# open http://localhost:8000
```

To refresh the satellite snapshot manually: `python3 scripts/fetch_ndvi.py`

## Data sources & methodology

- **Vegetation data:** NASA MODIS Terra MOD13Q1 via ORNL DAAC / NASA LP DAAC
- **Risk model** informed by CAAS (Chinese Academy of Agricultural Sciences) post-harvest training material and FAO post-harvest loss studies for South Asian supply chains (Ahmad et al. 2021; ADB 2019), as cited in the app
- NDVI health thresholds are calibrated per crop; the app labels every reading with its source and acquisition date

## Roadmap

- District-level push alerts (SMS/WhatsApp) for high-risk harvest windows
- On-device NDVI from drone imagery for individual fields
- Market-price feeds for the economic calculator

## Author

**Kashif Sajjad Khan** — [GitHub](https://github.com/kashifsajjadkhan) · Kashifsajjad7172@gmail.com

Built for agricultural extension officers and smallholder farmers in Pakistan. Open to collaboration, especially on applied remote sensing for agriculture.

## License

CC BY-NC 4.0 — see [LICENSE](LICENSE).
