# API & Data Extraction Examples

This document details the external API endpoints integrated by **s-MeteoRisk**, the request/response payloads, and the analytical database interface.

---

## 1. Open-Meteo Weather Forecast API

### Endpoint Specification
- **Method**: `GET`
- **URL**: `https://api.open-meteo.com/v1/forecast`
- **Purpose**: Fetch 7-day daily weather forecasts and meteorological indicators for Moroccan cities.
- **Extraction Module**: [`extraction/extract_bronze.py`](../extraction/extract_bronze.py)

### Example Request (Casablanca)
```http
GET /v1/forecast?latitude=33.5992&longitude=-7.62&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=auto HTTP/1.1
Host: api.open-meteo.com
Accept: application/json
```

```bash
curl -X GET "https://api.open-meteo.com/v1/forecast?latitude=33.5992&longitude=-7.6200&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=auto"
```

### Example Real Response (Truncated Sample)
```json
{
  "latitude": 33.6,
  "longitude": -7.625,
  "generationtime_ms": 0.12,
  "utc_offset_seconds": 3600,
  "timezone": "Africa/Casablanca",
  "timezone_abbreviation": "+01",
  "elevation": 27.0,
  "daily_units": {
    "time": "iso8601",
    "temperature_2m_max": "°C",
    "temperature_2m_min": "°C",
    "precipitation_sum": "mm",
    "precipitation_probability_max": "%",
    "wind_speed_10m_max": "km/h",
    "wind_gusts_10m_max": "km/h",
    "weather_code": "wmo code"
  },
  "daily": {
    "time": [
      "2026-09-15",
      "2026-09-16",
      "2026-09-17",
      "2026-09-18",
      "2026-09-19",
      "2026-09-20",
      "2026-09-21"
    ],
    "temperature_2m_max": [27.4, 26.8, 28.1, 29.5, 27.0, 26.2, 25.8],
    "temperature_2m_min": [18.2, 17.9, 18.5, 19.1, 18.0, 17.4, 16.9],
    "precipitation_sum": [0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0],
    "precipitation_probability_max": [5, 10, 0, 25, 5, 0, 0],
    "wind_speed_10m_max": [19.8, 22.1, 18.5, 24.2, 21.0, 17.5, 18.2],
    "wind_gusts_10m_max": [38.5, 42.1, 35.6, 48.2, 41.0, 34.2, 36.0],
    "weather_code": [0, 1, 0, 2, 1, 0, 0]
  },
  "city": "Casablanca"
}
```

---

## 2. PostgreSQL Gold Layer Interface

The Gold layer structures data into normalized relational tables for analytical queries.

### Cities Schema (`cities`)
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Auto Increment | Unique City ID |
| `name` | `VARCHAR(100)` | Unique, Not Null | City Name |
| `lat` | `FLOAT` | Not Null | Latitude Coordinate |
| `lng` | `FLOAT` | Not Null | Longitude Coordinate |

### Weather Risks Schema (`weather_risks`)
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Auto Increment | Unique Record ID |
| `city_id` | `INTEGER` | Foreign Key (`cities.id`) | Relational link to city |
| `date` | `DATE` | Not Null | Forecast Date |
| `temp_max` | `FLOAT` | Nullable | Max 2m Temperature (°C) |
| `precip_max` | `FLOAT` | Nullable | Max Precipitation Probability (%) |
| `wind_gusts` | `FLOAT` | Nullable | Peak Wind Gusts (km/h) |
| `risk_total` | `FLOAT` | Nullable | Composite Risk Score (0 - 100) |
| `temp_category` | `VARCHAR(50)` | Nullable | `Froid` (<15°C), `Modéré` (15-25°C), `Chaud` (>25°C) |
| `precip_category` | `VARCHAR(50)` | Nullable | `Faible` (<20%), `Moyenne` (20-60%), `Forte` (>60%) |
| `wind_category` | `VARCHAR(50)` | Nullable | `Calme` (<20 km/h), `Modéré` (20-50 km/h), `Fort` (>50 km/h) |

---

## 3. SQL Analytical Queries & Output

### Query: Highest Risk Moroccan Cities
```sql
SELECT c.name, ROUND(AVG(w.risk_total)::numeric, 2) AS avg_risk
FROM cities c
JOIN weather_risks w ON w.city_id = c.id
GROUP BY c.name
ORDER BY avg_risk DESC
LIMIT 5;
```

**Real Result:**
| City Name | Average Risk Score |
|---|---|
| Semara | 17.77 |
| Taroudannt | 15.73 |
| Laâyoune | 15.09 |
| Cabo Bojador | 14.80 |
| Oulad Teïma | 14.47 |

---

## 4. Airflow REST API (Optional Verification)
Apache Airflow exposes administrative REST endpoints on port 8080:
- Health check: `GET http://localhost:8080/health`
- DAG details: `GET http://localhost:8080/api/v1/dags/s_meteorisk_daily_update`
