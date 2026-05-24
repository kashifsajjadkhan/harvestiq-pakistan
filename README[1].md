# HarvestIQ-Pakistan 🌾🛰️

### *A Satellite-Driven Geospatial Decision-Support Framework for Agronomic Post-Harvest Supply Chain Stabilization*

---

[![Platform Status](https://img.shields.io/badge/Deployment-Live%20PWA-success?style=flat-square)](http://kashifsajjadkhan.github.io/harvestiq-pakistan)
[![Geospatial Data](https://img.shields.io/badge/Satellite--Data-MODIS%20%7C%20Sentinel--2-blue?style=flat-square)](#-core-computational-engine)
[![Target Core](https://img.shields.io/badge/Coverage-16%20Districts%20%28~73%25%29-orange?style=flat-square)](#-geospatial-scope-and-regional-calibration)
[![License](https://img.shields.io/badge/Open%20Science-MIT-lightgrey?style=flat-square)](#-academic-provenance-and-open-science)

🔗 **Production Environment URL:** [kashifsajjadkhan.github.io/harvestiq-pakistan](http://kashifsajjadkhan.github.io/harvestiq-pakistan)

---

## 📌 Executive Summary
Horticultural supply chains across developing agrarian economies experience significant vulnerabilities; macro-level estimations indicate that post-harvest logistical friction accounts for systemic volume losses between 40% and 80% within Pakistan's local distribution infrastructure. 

**HarvestIQ-Pakistan** addresses this diagnostic critical gap. Operating as an edge-computed, offline-capable Progressive Web App (PWA), this framework decodes multi-spectral macro-telemetry into actionable micro-level insights. By coupling dynamic vegetation indices with empirical transport models, it provides localized shelf-life forecasting, risk identification, and loss-adjusted economic valuations directly to rural stakeholders.

---

## ⚡ Architectural Capabilities & Technical Specifications

* **Multi-Scale Ingestion Pipeline:** Automated parsing of heterogeneous telemetry, blending low-spatial/high-temporal NASA MODIS Terra (1 km spatial resolution, 16-day composite) with high-spatial ESA Sentinel-2 (10 m spatial resolution) data bands.
* **Dynamic Phenological Baseline Mapping:** Replaces static vegetation models with empirical crop-specific lookup thresholds across 5 high-value horticultural baselines (Chilli, Tomato, Watermelon, Mango, Potato).
* **Multi-Criteria Evaluation (MCE) Matrix:** Processes a 9-variable client-side scoring array integrating satellite vegetative trends with farmer-inputted ambient metrics (e.g., storage microclimate, thermal profiling, packaging metrics, and transit latency).
* **Loss-Adjusted Financial Predictive Analytics:** Executes multi-variant economic forecasting models to compute true financial exposure parameters ($L_{PKR}$), mitigative retention margins ($L_{saved}$), and moving asset break-even cost adjustments ($P_{BE}$).
* **Resilient Infrastructure Design:** Built utilizing a lightweight client-side script base with an embedded bilingual (English/Urdu) localized configuration, ensuring structural uptime within severe bandwidth-constrained rural topologies.

---

## 🛠️ System Architecture & Data Flow

The layout below illustrates the logical boundaries between the remote data ingestion tiers, client-side algorithm executions, and down-stream predictive indicators:

```text
  [ GEOSPATIAL & USER INPUTS ]              [ CLIENT ENGINE PROCESSING ]               [ ANALYTIC OUTPUTS ]
  +--------------------------+              +------------------------------+          +-------------------------+
  |  NASA MODIS / Sentinel   |              | Phase 1:                     |          | Real-Time Bilingual UI  |
  |  Multi-Spectral Radiance |------------->| Crop-Specific NDVI Parsing   |--------->| Diagnostic Heat Maps    |
  +--------------------------+              +------------------------------+          +-------------------------+
                                                           |                                       |
  +--------------------------+                             v                                       v
  |  9-Variable Field Data   |              +------------------------------+          +-------------------------+
  |  (Storage, Temp, Logistics)------------>| Phase 2:                     |--------->| Target Shelf Life ($S_{adj}$) |
  +--------------------------+              | Weighted Spoilage Matrix ($R$)|          | Economic Risk ($L_{PKR}$) |
                                            +------------------------------+          | Break-Even ($P_{BE}$)    |
  +--------------------------+                             ^                          +-------------------------+
  |  Live Commodity Market   |-----------------------------+
  |  Price Feed (PKR)        |
  +--------------------------+# HarvestIQ-Pakistan 🌾🛰️

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
