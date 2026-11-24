# Argus ANPR Benchmark Report

**Date**: 2026-11-24 18:41:04  
**Dataset**: `tests/images` (57 images)

## 1. Summary Metrics

| Metric | Value |
|---|---|
| **Total Images Processed** | 57 |
| **Images with Plate(s)** | 57 (100.0%) |
| **Images without Plate** | 0 (0.0%) |
| **Total Plates Detected** | 62 |
| **Total Wall Duration** | 9.55 s |
| **Mean Latency** | 167.54 ms |
| **Median (P50) Latency** | 100.92 ms |
| **Min Latency** | 90.00 ms |
| **Max Latency** | 644.64 ms |
| **P95 Latency** | 413.90 ms |
| **P99 Latency** | 644.64 ms |

## 2. Latency Tier Breakdown

| Tier | Latency Range | Count | Percentage |
|---|---|---|---|
| **Fast-ALPR Full-Frame** | $\le 50\text{ ms}$ | 0 | 0.0% |
| **Crop / Secondary Tier** | $50\text{--}200\text{ ms}$ | 45 | 78.9% |
| **RapidOCR Fallback Tier** | $> 200\text{ ms}$ | 12 | 21.1% |

## 3. Detailed Results per Image

| # | Image | Plates Detected | Latency (ms) | Speed Tier |
|---|---|---|---|---|
| 1 | `1.jpg` | `RJ14GT4976` | 148.45 | Crop (50-200ms) |
| 2 | `2.jpg` | `RJ09GA0165` | 115.00 | Crop (50-200ms) |
| 3 | `3.jpg` | `BP6A4904` | 158.48 | Crop (50-200ms) |
| 4 | `4.jpg` | `RJ43GA2012` | 644.64 | RapidOCR (>200ms) |
| 5 | `5.jpg` | `NL02K7556` | 363.27 | RapidOCR (>200ms) |
| 6 | `6.jpg` | `MH20DV2363` | 90.00 | Crop (50-200ms) |
| 7 | `7.jpg` | `HR69D4793` | 109.33 | Crop (50-200ms) |
| 8 | `8.jpg` | `UP24AT4598` | 116.76 | Crop (50-200ms) |
| 9 | `9.jpg` | `HR69F7084` | 109.21 | Crop (50-200ms) |
| 10 | `10.jpg` | `NL02K7556` | 352.12 | RapidOCR (>200ms) |
| 11 | `11.jpg` | `BP6A4904` | 148.43 | Crop (50-200ms) |
| 12 | `12.jpg` | `RJ43GA2012` | 395.63 | RapidOCR (>200ms) |
| 13 | `13.jpg` | `DL1CX2744` | 95.75 | Crop (50-200ms) |
| 14 | `14.jpg` | `DL1CX2744` | 95.84 | Crop (50-200ms) |
| 15 | `15.jpg` | `DL1CX2744` | 99.70 | Crop (50-200ms) |
| 16 | `16.jpg` | `DL1CX2744` | 95.37 | Crop (50-200ms) |
| 17 | `17.jpg` | `HR69S7084` | 96.42 | Crop (50-200ms) |
| 18 | `18.jpg` | `HR69F7084` | 99.35 | Crop (50-200ms) |
| 19 | `19.jpg` | `HR69F7084` | 96.75 | Crop (50-200ms) |
| 20 | `20.jpg` | `HR69F7084` | 95.85 | Crop (50-200ms) |
| 21 | `21.jpg` | `DL1CX2744` | 96.08 | Crop (50-200ms) |
| 22 | `22.jpg` | `DL1CX2744` | 95.83 | Crop (50-200ms) |
| 23 | `23.jpg` | `DL1CX2744` | 96.51 | Crop (50-200ms) |
| 24 | `24.jpg` | `UP24A7459` | 98.23 | Crop (50-200ms) |
| 25 | `25.jpg` | `HR398733`, `HR39G8733`, `HR89G8733` | 396.93 | RapidOCR (>200ms) |
| 26 | `26.jpg` | `HR39G8733` | 100.92 | Crop (50-200ms) |
| 27 | `27.jpg` | `HR39G8733` | 97.15 | Crop (50-200ms) |
| 28 | `28.jpg` | `HR39G8733`, `HR69TEN4400` | 393.41 | RapidOCR (>200ms) |
| 29 | `29.jpg` | `DL1CX2744` | 96.21 | Crop (50-200ms) |
| 30 | `30.jpg` | `DL1GE3496` | 98.83 | Crop (50-200ms) |
| 31 | `31.jpg` | `HR63D4286` | 347.39 | RapidOCR (>200ms) |
| 32 | `32.jpg` | `HR63G4286` | 102.92 | Crop (50-200ms) |
| 33 | `33.jpg` | `HR5B0358` | 96.70 | Crop (50-200ms) |
| 34 | `34.jpg` | `HR58D3586` | 158.84 | Crop (50-200ms) |
| 35 | `35.jpg` | `UP81DT2591` | 97.82 | Crop (50-200ms) |
| 36 | `36.jpg` | `DL1GE3496` | 145.06 | Crop (50-200ms) |
| 37 | `37.jpg` | `DL1GE3496` | 120.35 | Crop (50-200ms) |
| 38 | `38.jpg` | `DL1L4619`, `DL71A6992` | 111.06 | Crop (50-200ms) |
| 39 | `39.jpg` | `DL1LAE1928` | 93.23 | Crop (50-200ms) |
| 40 | `40.jpg` | `HR63G4286` | 97.91 | Crop (50-200ms) |
| 41 | `41.jpg` | `HR63D4286`, `HR63G4886` | 412.28 | RapidOCR (>200ms) |
| 42 | `42.jpg` | `HR58D3586` | 97.53 | Crop (50-200ms) |
| 43 | `43.jpg` | `HR58D3586` | 365.55 | RapidOCR (>200ms) |
| 44 | `44.jpg` | `UP81D7259` | 147.89 | Crop (50-200ms) |
| 45 | `45.jpg` | `DL1LAE1928` | 154.58 | Crop (50-200ms) |
| 46 | `46.jpg` | `DL1LAE1328` | 428.52 | RapidOCR (>200ms) |
| 47 | `47.jpg` | `UP14PT2007` | 95.10 | Crop (50-200ms) |
| 48 | `48.jpg` | `RJ11GC1682` | 234.48 | RapidOCR (>200ms) |
| 49 | `49.jpg` | `UP14PT2007` | 93.07 | Crop (50-200ms) |
| 50 | `50.jpg` | `DL1L4519` | 102.31 | Crop (50-200ms) |
| 51 | `51.jpg` | `DL1LAE1928` | 97.66 | Crop (50-200ms) |
| 52 | `52.jpg` | `DL1LAE1928` | 97.59 | Crop (50-200ms) |
| 53 | `53.jpg` | `DL1MR0230` | 100.66 | Crop (50-200ms) |
| 54 | `54.jpg` | `DL1NA0230` | 96.78 | Crop (50-200ms) |
| 55 | `55.jpg` | `DL1NA0230` | 353.19 | RapidOCR (>200ms) |
| 56 | `56.jpg` | `DL1MA0230` | 95.11 | Crop (50-200ms) |
| 57 | `57.jpg` | `RJ11GC1682` | 109.90 | Crop (50-200ms) |
