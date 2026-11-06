# Pipeline Execution & Risk Analysis Metrics

This report summarizes verified quantitative metrics from the **s-MeteoRisk** data pipeline across Moroccan cities.

---

## 1. Dataset Dimensions & Coverage

| Metric | Verified Value | Description |
|---|---|---|
| **Coverage Area** | Morocco (120 municipalities) | Geographically distributed across all 12 administrative regions |
| **Active Forecast Window** | 7-day rolling window | Daily forecasted metrics |
| **Bronze Layer Size** | 120 API JSON payloads | Raw response data preserved for auditability |
| **Silver Records** | 840 daily rows | Cleaned, deduplicated, and feature-engineered |
| **Gold Records (PostgreSQL)** | 1,800 historical/forecast rows | Loaded into relational star-like schema |

---

## 2. Feature Engineering & Risk Score Distribution

The composite risk score is evaluated across wind speed, extreme temperatures, and precipitation probabilities.

### Statistical Summary
| Metric | Wind Risk (`risk_wind`) | Rain Risk (`risk_rain`) | Temperature Risk (`risk_temp`) | Total Risk Score (`risk_score_total`) |
|---|---|---|---|---|
| **Mean** | 3.29 | 0.85 | 0.21 | **4.35** |
| **Standard Deviation** | 6.59 | 2.58 | 2.06 | **8.02** |
| **Minimum** | 0.00 | 0.00 | 0.00 | **0.00** |
| **25th Percentile** | 0.00 | 0.00 | 0.00 | **0.00** |
| **Median (50%)** | 0.00 | 0.00 | 0.00 | **0.00** |
| **75th Percentile** | 0.00 | 0.30 | 0.00 | **3.00** |
| **Maximum** | 30.00 | 22.50 | 20.00 | **38.00** |

---

## 3. High-Risk Municipalities (Top 5 Ranked)

| Rank | Municipality | Avg Total Risk Score | Primary Risk Factor | Peak Temperature | Max Precip. Prob. |
|---|---|---|---|---|---|
| 1 | **Semara** | 17.77 | Extreme Heat + Gusts | 41.9 °C | 15.0 % |
| 2 | **Taroudannt** | 15.73 | Thermal Anomaly (>40°C) | 40.5 °C | 18.0 % |
| 3 | **Laâyoune** | 15.09 | Saharan High Temperature | 42.3 °C | 12.0 % |
| 4 | **Cabo Bojador** | 14.80 | Coastal Wind Gusts | 34.1 °C | 20.0 % |
| 5 | **Oulad Teïma** | 14.47 | Extreme Heat Index | 40.3 °C | 15.0 % |

---

## 4. Precipitation Hotspots (Top 5 Ranked)

| Rank | Municipality | Peak Precipitation Probability | Max Rainfall Event |
|---|---|---|---|
| 1 | **Bou Arfa** | 75.0 % | High convective rain event |
| 2 | **Tineghir** | 70.0 % | Mountain precipitation |
| 3 | **Errachidia** | 68.0 % | Desert fringe storm pattern |
| 4 | **Jerada** | 60.0 % | High plateau precipitation |
| 5 | **Midalt** | 58.0 % | Atlas mountain front |
