# HarvestIQ-Pakistan 🌾🛰️

**A Satellite-Integrated, Client-Side Post-Harvest Loss Prediction & Decision-Support System for Smallholder Farmers.**

🚀 **Live Application:** [kashifsajjadkhan.github.io/harvestiq-pakistan](http://kashifsajjadkhan.github.io/harvestiq-pakistan)

---

## 📌 Project Overview
Pakistan loses between 40% and 80% of its horticultural produce annually due to inefficiencies in the supply chain, costing the economy over USD 1 billion per year. **HarvestIQ-Pakistan** bridges the gap between high-level institutional satellite data and smallholder farmers by providing real-time, district-level data to project shelf life, assess spoilage risks, and calculate financial impacts.

The platform is explicitly engineered as an **offline-capable Progressive Web App (PWA)** featuring a bilingual (English/Urdu) interface, making it fully operational in low-connectivity rural agricultural zones.

---

## ⚡ Key Features
* **Multi-Scale Satellite Monitoring:** Ingests NASA MODIS Terra (1 km resolution) and ESA Sentinel-2 (10 m resolution) telemetry to compute near-real-time NDVI crop-canopy health indexes.
* **Crop-Specific Threshold Analysis:** Evaluates live vegetation health using independent, calibrated lookup baselines across 5 core commodities (Chilli, Tomato, Watermelon, Mango, Potato).
* **9-Variable Weighted Spoilage Matrix:** Combines remote sensing data with user-inputted microclimate and logistics conditions (maturity stage, packaging, ambient temperature, humidity, and transport method).
* **Loss-Adjusted Financial Analytics:** Generates actionable PKR-denominated economic loss estimates ($L_{PKR}$), potential CAAS-aligned intervention savings ($L_{saved}$), and loss-adjusted target Break-Even Prices ($P_{BE}$).
* **Macro Geographic Coverage:** Actively tracks and models data across 16 major agricultural districts covering ~73% of Pakistan's commercial horticultural market output.

---

## 🛠️ System Architecture & Workflow

```text
[ INPUT TIERS ]                         [ CLIENT-SIDE PROCESSING LAYER ]          [ ACTIONABLE OUTPUTS ]
+-------------------------+             +-------------------------------+         +----------------------------+
| NASA MODIS (1km)        |------------>| Phase 1:                      |        | Bilingual UI (Urdu/English)|
| ESA Sentinel-2 (10m)    |             | Crop-Specific NDVI            |-------->| Color-Coded Health Maps    |
+-------------------------+             | Classification Tables         |         +----------------------------+
                                        +-------------------------------+                       |
+-------------------------+                             |                                       v
| 9-Variable User Inputs  |                             v                         +----------------------------+
| (Storage, Temp, etc.)   |------------>| Phase 2:                      |-------->| Projections & Shelf Life   |
+-------------------------+             | Weighted Spoilage             |         | Calculated Loss (PKR)      |
                                        | Risk Matrix Calculation ($R$)   |         | Loss-Adjusted Break-Even   |
+-------------------------+             +-------------------------------+         +----------------------------+
| Live Market Prices      |-----------------------------+
+-------------------------+# HarvestIQ-Pakistan 🌾🛰️

**A Satellite-Integrated, Client-Side Post-Harvest Loss Prediction & Decision-Support System for Smallholder Farmers.**

🚀 **Live Application:** [kashifsajjadkhan.github.io/harvestiq-pakistan](http://kashifsajjadkhan.github.io/harvestiq-pakistan)

---

## 📌 Project Overview
Pakistan loses between 40% and 80% of its horticultural produce annually due to inefficiencies in the supply chain, costing the economy over USD 1 billion per year. **HarvestIQ-Pakistan** bridges the gap between high-level institutional satellite data and smallholder farmers by providing real-time, district-level data to project shelf life, assess spoilage risks, and calculate financial impacts.

The platform is explicitly engineered as an **offline-capable Progressive Web App (PWA)** featuring a bilingual (English/Urdu) interface, making it fully operational in low-connectivity rural agricultural zones.

---

## ⚡ Key Features
* **Multi-Scale Satellite Monitoring:** Ingests NASA MODIS Terra (1 km resolution) and ESA Sentinel-2 (10 m resolution) telemetry to compute near-real-time NDVI crop-canopy health indexes.
* **Crop-Specific Threshold Analysis:** Evaluates live vegetation health using independent, calibrated lookup baselines across 5 core commodities (Chilli, Tomato, Watermelon, Mango, Potato).
* **9-Variable Weighted Spoilage Matrix:** Combines remote sensing data with user-inputted microclimate and logistics conditions (maturity stage, packaging, ambient temperature, humidity, and transport method).
* **Loss-Adjusted Financial Analytics:** Generates actionable PKR-denominated economic loss estimates ($L_{PKR}$), potential CAAS-aligned intervention savings ($L_{saved}$), and loss-adjusted target Break-Even Prices ($P_{BE}$).
* **Macro Geographic Coverage:** Actively tracks and models data across 16 major agricultural districts covering ~73% of Pakistan's commercial horticultural market output.

---

## 🛠️ System Architecture & Workflow
