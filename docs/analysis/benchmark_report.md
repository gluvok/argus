# Argus ANPR Benchmark Report

**Date**: 2026-11-18 22:17:03  
**Dataset**: `tests/images` (57 images)

## 1. Summary Metrics

| Metric | Value |
|---|---|
| **Total Images Processed** | 57 |
| **Images with Plate(s)** | 57 (100.0%) |
| **Images without Plate** | 0 (0.0%) |
| **Total Plates Detected** | 60 |
| **Total Wall Duration** | 6.15 s |
| **Mean Latency** | 107.81 ms |
| **Median (P50) Latency** | 74.94 ms |
| **Min Latency** | 60.89 ms |
| **Max Latency** | 290.72 ms |
| **P95 Latency** | 269.32 ms |
| **P99 Latency** | 290.72 ms |

## 2. Latency Tier Breakdown

| Tier | Latency Range | Count | Percentage |
|---|---|---|---|
| **Fast-ALPR Full-Frame** | $\le 50\text{ ms}$ | 0 | 0.0% |
| **Crop / Secondary Tier** | $50\text{--}200\text{ ms}$ | 48 | 84.2% |
| **RapidOCR Fallback Tier** | $> 200\text{ ms}$ | 9 | 15.8% |

## 3. Detailed Results per Image

| # | Image | Plates Detected | Latency (ms) | Speed Tier |
|---|---|---|---|---|
| 1 | `1.jpg` | `RJ14GT4976` | 79.64 | Crop (50-200ms) |
| 2 | `2.jpg` | `RJ09GA0165` | 76.76 | Crop (50-200ms) |
| 3 | `3.jpg` | `BP6A4904` | 120.56 | Crop (50-200ms) |
| 4 | `4.jpg` | `RJ43GA2012` | 268.59 | RapidOCR (>200ms) |
| 5 | `5.jpg` | `NL02K7556` | 213.11 | RapidOCR (>200ms) |
| 6 | `6.jpg` | `MH20DV2363` | 60.89 | Crop (50-200ms) |
| 7 | `7.jpg` | `HR69D4793` | 71.90 | Crop (50-200ms) |
| 8 | `8.jpg` | `UP24AT4598` | 70.22 | Crop (50-200ms) |
| 9 | `9.jpg` | `HR69F7084` | 74.94 | Crop (50-200ms) |
| 10 | `10.jpg` | `NL02K7556` | 193.86 | Crop (50-200ms) |
| 11 | `11.jpg` | `BP6A4904` | 106.67 | Crop (50-200ms) |
| 12 | `12.jpg` | `RJ43GA2012` | 257.35 | RapidOCR (>200ms) |
| 13 | `13.jpg` | `DL1CX2744` | 67.71 | Crop (50-200ms) |
| 14 | `14.jpg` | `DL1CX2744` | 83.74 | Crop (50-200ms) |
| 15 | `15.jpg` | `DL1CX2744` | 72.77 | Crop (50-200ms) |
| 16 | `16.jpg` | `DL1CX2744` | 66.96 | Crop (50-200ms) |
| 17 | `17.jpg` | `HR69S7084` | 70.84 | Crop (50-200ms) |
| 18 | `18.jpg` | `HR69F7084` | 64.86 | Crop (50-200ms) |
| 19 | `19.jpg` | `HR69F7084` | 65.99 | Crop (50-200ms) |
| 20 | `20.jpg` | `HR69F7084` | 64.62 | Crop (50-200ms) |
| 21 | `21.jpg` | `DL1CX2744` | 62.84 | Crop (50-200ms) |
| 22 | `22.jpg` | `DL1CX2744` | 62.80 | Crop (50-200ms) |
| 23 | `23.jpg` | `DL1CX2744` | 62.81 | Crop (50-200ms) |
| 24 | `24.jpg` | `UP24A7459` | 63.71 | Crop (50-200ms) |
| 25 | `25.jpg` | `HR694873` | 63.39 | Crop (50-200ms) |
| 26 | `26.jpg` | `HR39G8733` | 97.13 | Crop (50-200ms) |
| 27 | `27.jpg` | `HR39G8733` | 110.27 | Crop (50-200ms) |
| 28 | `28.jpg` | `HR39G8733`, `HR69TEN4400` | 275.90 | RapidOCR (>200ms) |
| 29 | `29.jpg` | `DL1CX2744` | 78.31 | Crop (50-200ms) |
| 30 | `30.jpg` | `DL1GE3496` | 89.55 | Crop (50-200ms) |
| 31 | `31.jpg` | `HR63D4286` | 238.43 | RapidOCR (>200ms) |
| 32 | `32.jpg` | `HR63G4286` | 76.62 | Crop (50-200ms) |
| 33 | `33.jpg` | `HR5B0358` | 74.11 | Crop (50-200ms) |
| 34 | `34.jpg` | `HR58D3586` | 74.66 | Crop (50-200ms) |
| 35 | `35.jpg` | `UP81DT2591` | 72.46 | Crop (50-200ms) |
| 36 | `36.jpg` | `DL1GE3496` | 76.68 | Crop (50-200ms) |
| 37 | `37.jpg` | `DL1GE3496` | 85.44 | Crop (50-200ms) |
| 38 | `38.jpg` | `DL1L4619`, `DL71A6992` | 76.71 | Crop (50-200ms) |
| 39 | `39.jpg` | `DL1LAE1928` | 73.80 | Crop (50-200ms) |
| 40 | `40.jpg` | `HR63G4286` | 75.02 | Crop (50-200ms) |
| 41 | `41.jpg` | `HR63D4286`, `HR63G4886` | 245.31 | RapidOCR (>200ms) |
| 42 | `42.jpg` | `HR58D3586` | 69.14 | Crop (50-200ms) |
| 43 | `43.jpg` | `HR58D3586` | 249.40 | RapidOCR (>200ms) |
| 44 | `44.jpg` | `UP81D7259` | 126.59 | Crop (50-200ms) |
| 45 | `45.jpg` | `DL1LAE1928` | 74.87 | Crop (50-200ms) |
| 46 | `46.jpg` | `DL1LAE1328` | 290.72 | RapidOCR (>200ms) |
| 47 | `47.jpg` | `UP14PT2007` | 67.23 | Crop (50-200ms) |
| 48 | `48.jpg` | `RJ11GC1682` | 152.38 | Crop (50-200ms) |
| 49 | `49.jpg` | `UP14PT2007` | 69.00 | Crop (50-200ms) |
| 50 | `50.jpg` | `DL1L4519` | 69.94 | Crop (50-200ms) |
| 51 | `51.jpg` | `DL1LAE1928` | 74.61 | Crop (50-200ms) |
| 52 | `52.jpg` | `DL1LAE1928` | 85.96 | Crop (50-200ms) |
| 53 | `53.jpg` | `DL1MR0230` | 86.55 | Crop (50-200ms) |
| 54 | `54.jpg` | `DL1NA0230` | 72.89 | Crop (50-200ms) |
| 55 | `55.jpg` | `DL1NA0230` | 230.30 | RapidOCR (>200ms) |
| 56 | `56.jpg` | `DL1MA0230` | 65.97 | Crop (50-200ms) |
| 57 | `57.jpg` | `RJ11GC1682` | 71.73 | Crop (50-200ms) |
