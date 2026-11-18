# Argus ANPR Benchmark Report

**Date**: 2026-11-18 22:10:13  
**Dataset**: `tests/images` (57 images)

## 1. Summary Metrics

| Metric | Value |
|---|---|
| **Total Images Processed** | 57 |
| **Images with Plate(s)** | 57 (100.0%) |
| **Images without Plate** | 0 (0.0%) |
| **Total Plates Detected** | 60 |
| **Total Wall Duration** | 5.25 s |
| **Mean Latency** | 92.09 ms |
| **Median (P50) Latency** | 63.24 ms |
| **Min Latency** | 57.08 ms |
| **Max Latency** | 248.54 ms |
| **P95 Latency** | 225.03 ms |
| **P99 Latency** | 248.54 ms |

## 2. Latency Tier Breakdown

| Tier | Latency Range | Count | Percentage |
|---|---|---|---|
| **Fast-ALPR Full-Frame** | $\le 50\text{ ms}$ | 0 | 0.0% |
| **Crop / Secondary Tier** | $50\text{--}200\text{ ms}$ | 53 | 93.0% |
| **RapidOCR Fallback Tier** | $> 200\text{ ms}$ | 4 | 7.0% |

## 3. Detailed Results per Image

| # | Image | Plates Detected | Latency (ms) | Speed Tier |
|---|---|---|---|---|
| 1 | `1.jpg` | `RJ14GT4976` | 68.52 | Crop (50-200ms) |
| 2 | `2.jpg` | `RJ09GA0165` | 65.73 | Crop (50-200ms) |
| 3 | `3.jpg` | `BP6A4904` | 104.17 | Crop (50-200ms) |
| 4 | `4.jpg` | `RJ43GA2012` | 248.54 | RapidOCR (>200ms) |
| 5 | `5.jpg` | `NL02K7556` | 199.78 | Crop (50-200ms) |
| 6 | `6.jpg` | `MH20DV2363` | 57.08 | Crop (50-200ms) |
| 7 | `7.jpg` | `HR69D4793` | 65.87 | Crop (50-200ms) |
| 8 | `8.jpg` | `UP24AT4598` | 66.94 | Crop (50-200ms) |
| 9 | `9.jpg` | `HR69F7084` | 74.72 | Crop (50-200ms) |
| 10 | `10.jpg` | `NL02K7556` | 194.56 | Crop (50-200ms) |
| 11 | `11.jpg` | `BP6A4904` | 103.80 | Crop (50-200ms) |
| 12 | `12.jpg` | `RJ43GA2012` | 246.73 | RapidOCR (>200ms) |
| 13 | `13.jpg` | `DL1CX2744` | 66.93 | Crop (50-200ms) |
| 14 | `14.jpg` | `DL1CX2744` | 62.82 | Crop (50-200ms) |
| 15 | `15.jpg` | `DL1CX2744` | 61.89 | Crop (50-200ms) |
| 16 | `16.jpg` | `DL1CX2744` | 62.62 | Crop (50-200ms) |
| 17 | `17.jpg` | `HR69S7084` | 62.70 | Crop (50-200ms) |
| 18 | `18.jpg` | `HR69F7084` | 63.27 | Crop (50-200ms) |
| 19 | `19.jpg` | `HR69F7084` | 61.28 | Crop (50-200ms) |
| 20 | `20.jpg` | `HR69F7084` | 61.15 | Crop (50-200ms) |
| 21 | `21.jpg` | `DL1CX2744` | 62.12 | Crop (50-200ms) |
| 22 | `22.jpg` | `DL1CX2744` | 63.07 | Crop (50-200ms) |
| 23 | `23.jpg` | `DL1CX2744` | 62.62 | Crop (50-200ms) |
| 24 | `24.jpg` | `UP24A7459` | 62.96 | Crop (50-200ms) |
| 25 | `25.jpg` | `HR694873` | 60.44 | Crop (50-200ms) |
| 26 | `26.jpg` | `HR39G8733` | 61.80 | Crop (50-200ms) |
| 27 | `27.jpg` | `HR39G8733` | 65.80 | Crop (50-200ms) |
| 28 | `28.jpg` | `HR39G8733`, `HR69TEN4400` | 220.55 | RapidOCR (>200ms) |
| 29 | `29.jpg` | `DL1CX2744` | 61.76 | Crop (50-200ms) |
| 30 | `30.jpg` | `DL1GE3496` | 64.30 | Crop (50-200ms) |
| 31 | `31.jpg` | `HR63D4286` | 179.85 | Crop (50-200ms) |
| 32 | `32.jpg` | `HR63G4286` | 61.69 | Crop (50-200ms) |
| 33 | `33.jpg` | `HR5B0358` | 61.49 | Crop (50-200ms) |
| 34 | `34.jpg` | `HR58D3586` | 62.51 | Crop (50-200ms) |
| 35 | `35.jpg` | `UP81DT2591` | 62.02 | Crop (50-200ms) |
| 36 | `36.jpg` | `DL1GE3496` | 63.24 | Crop (50-200ms) |
| 37 | `37.jpg` | `DL1GE3496` | 62.71 | Crop (50-200ms) |
| 38 | `38.jpg` | `DL1L4619`, `DL71A6992` | 68.30 | Crop (50-200ms) |
| 39 | `39.jpg` | `DL1LAE1928` | 61.38 | Crop (50-200ms) |
| 40 | `40.jpg` | `HR63G4286` | 62.65 | Crop (50-200ms) |
| 41 | `41.jpg` | `HR63D4286`, `HR63G4886` | 194.15 | Crop (50-200ms) |
| 42 | `42.jpg` | `HR58D3586` | 59.12 | Crop (50-200ms) |
| 43 | `43.jpg` | `HR58D3586` | 198.11 | Crop (50-200ms) |
| 44 | `44.jpg` | `UP81D7259` | 101.37 | Crop (50-200ms) |
| 45 | `45.jpg` | `DL1LAE1928` | 63.36 | Crop (50-200ms) |
| 46 | `46.jpg` | `DL1LAE1328` | 222.62 | RapidOCR (>200ms) |
| 47 | `47.jpg` | `UP14PT2007` | 59.23 | Crop (50-200ms) |
| 48 | `48.jpg` | `RJ11GC1682` | 127.36 | Crop (50-200ms) |
| 49 | `49.jpg` | `UP14PT2007` | 59.27 | Crop (50-200ms) |
| 50 | `50.jpg` | `DL1L4519` | 63.87 | Crop (50-200ms) |
| 51 | `51.jpg` | `DL1LAE1928` | 61.89 | Crop (50-200ms) |
| 52 | `52.jpg` | `DL1LAE1928` | 61.61 | Crop (50-200ms) |
| 53 | `53.jpg` | `DL1MR0230` | 63.51 | Crop (50-200ms) |
| 54 | `54.jpg` | `DL1NA0230` | 62.05 | Crop (50-200ms) |
| 55 | `55.jpg` | `DL1NA0230` | 193.25 | Crop (50-200ms) |
| 56 | `56.jpg` | `DL1MA0230` | 62.75 | Crop (50-200ms) |
| 57 | `57.jpg` | `RJ11GC1682` | 65.26 | Crop (50-200ms) |
