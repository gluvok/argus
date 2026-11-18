# Argus ANPR Benchmark Report

**Date**: 2026-11-18 22:06:53  
**Dataset**: `tests/images` (57 images)

## 1. Summary Metrics

| Metric | Value |
|---|---|
| **Total Images Processed** | 57 |
| **Images with Plate(s)** | 57 (100.0%) |
| **Images without Plate** | 0 (0.0%) |
| **Total Plates Detected** | 60 |
| **Total Wall Duration** | 5.37 s |
| **Mean Latency** | 94.27 ms |
| **Median (P50) Latency** | 63.86 ms |
| **Min Latency** | 58.51 ms |
| **Max Latency** | 293.90 ms |
| **P95 Latency** | 239.58 ms |
| **P99 Latency** | 293.90 ms |

## 2. Latency Tier Breakdown

| Tier | Latency Range | Count | Percentage |
|---|---|---|---|
| **Fast-ALPR Full-Frame** | $\le 50\text{ ms}$ | 0 | 0.0% |
| **Crop / Secondary Tier** | $50\text{--}200\text{ ms}$ | 50 | 87.7% |
| **RapidOCR Fallback Tier** | $> 200\text{ ms}$ | 7 | 12.3% |

## 3. Detailed Results per Image

| # | Image | Plates Detected | Latency (ms) | Speed Tier |
|---|---|---|---|---|
| 1 | `1.jpg` | `RJ14GT4976` | 67.21 | Crop (50-200ms) |
| 2 | `2.jpg` | `RJ09GA0165` | 66.41 | Crop (50-200ms) |
| 3 | `3.jpg` | `BP6A4904` | 111.17 | Crop (50-200ms) |
| 4 | `4.jpg` | `RJ43GA2012` | 293.90 | RapidOCR (>200ms) |
| 5 | `5.jpg` | `NL02K7556` | 209.16 | RapidOCR (>200ms) |
| 6 | `6.jpg` | `MH20DV2363` | 58.92 | Crop (50-200ms) |
| 7 | `7.jpg` | `HR69D4793` | 66.08 | Crop (50-200ms) |
| 8 | `8.jpg` | `UP24AT4598` | 68.53 | Crop (50-200ms) |
| 9 | `9.jpg` | `HR69F7084` | 68.61 | Crop (50-200ms) |
| 10 | `10.jpg` | `NL02K7556` | 187.55 | Crop (50-200ms) |
| 11 | `11.jpg` | `BP6A4904` | 101.17 | Crop (50-200ms) |
| 12 | `12.jpg` | `RJ43GA2012` | 239.15 | RapidOCR (>200ms) |
| 13 | `13.jpg` | `DL1CX2744` | 62.87 | Crop (50-200ms) |
| 14 | `14.jpg` | `DL1CX2744` | 64.20 | Crop (50-200ms) |
| 15 | `15.jpg` | `DL1CX2744` | 63.47 | Crop (50-200ms) |
| 16 | `16.jpg` | `DL1CX2744` | 65.05 | Crop (50-200ms) |
| 17 | `17.jpg` | `HR69S7084` | 63.70 | Crop (50-200ms) |
| 18 | `18.jpg` | `HR69F7084` | 64.63 | Crop (50-200ms) |
| 19 | `19.jpg` | `HR69F7084` | 63.24 | Crop (50-200ms) |
| 20 | `20.jpg` | `HR69F7084` | 63.40 | Crop (50-200ms) |
| 21 | `21.jpg` | `DL1CX2744` | 63.01 | Crop (50-200ms) |
| 22 | `22.jpg` | `DL1CX2744` | 63.20 | Crop (50-200ms) |
| 23 | `23.jpg` | `DL1CX2744` | 63.16 | Crop (50-200ms) |
| 24 | `24.jpg` | `UP24A7459` | 63.69 | Crop (50-200ms) |
| 25 | `25.jpg` | `HR694873` | 61.82 | Crop (50-200ms) |
| 26 | `26.jpg` | `HR39G8733` | 62.82 | Crop (50-200ms) |
| 27 | `27.jpg` | `HR39G8733` | 65.74 | Crop (50-200ms) |
| 28 | `28.jpg` | `HR39G8733`, `HR69TEN4400` | 221.39 | RapidOCR (>200ms) |
| 29 | `29.jpg` | `DL1CX2744` | 67.10 | Crop (50-200ms) |
| 30 | `30.jpg` | `DL1GE3496` | 63.53 | Crop (50-200ms) |
| 31 | `31.jpg` | `HR63D4286` | 181.94 | Crop (50-200ms) |
| 32 | `32.jpg` | `HR63G4286` | 58.51 | Crop (50-200ms) |
| 33 | `33.jpg` | `HR5B0358` | 62.13 | Crop (50-200ms) |
| 34 | `34.jpg` | `HR58D3586` | 62.69 | Crop (50-200ms) |
| 35 | `35.jpg` | `UP81DT2591` | 61.73 | Crop (50-200ms) |
| 36 | `36.jpg` | `DL1GE3496` | 63.64 | Crop (50-200ms) |
| 37 | `37.jpg` | `DL1GE3496` | 62.90 | Crop (50-200ms) |
| 38 | `38.jpg` | `DL1L4619`, `DL71A6992` | 63.87 | Crop (50-200ms) |
| 39 | `39.jpg` | `DL1LAE1928` | 63.08 | Crop (50-200ms) |
| 40 | `40.jpg` | `HR63G4286` | 62.82 | Crop (50-200ms) |
| 41 | `41.jpg` | `HR63D4286`, `HR63G4886` | 243.46 | RapidOCR (>200ms) |
| 42 | `42.jpg` | `HR58D3586` | 60.74 | Crop (50-200ms) |
| 43 | `43.jpg` | `HR58D3586` | 209.17 | RapidOCR (>200ms) |
| 44 | `44.jpg` | `UP81D7259` | 102.19 | Crop (50-200ms) |
| 45 | `45.jpg` | `DL1LAE1928` | 63.86 | Crop (50-200ms) |
| 46 | `46.jpg` | `DL1LAE1328` | 225.06 | RapidOCR (>200ms) |
| 47 | `47.jpg` | `UP14PT2007` | 65.03 | Crop (50-200ms) |
| 48 | `48.jpg` | `RJ11GC1682` | 127.32 | Crop (50-200ms) |
| 49 | `49.jpg` | `UP14PT2007` | 59.31 | Crop (50-200ms) |
| 50 | `50.jpg` | `DL1L4519` | 64.79 | Crop (50-200ms) |
| 51 | `51.jpg` | `DL1LAE1928` | 62.10 | Crop (50-200ms) |
| 52 | `52.jpg` | `DL1LAE1928` | 62.23 | Crop (50-200ms) |
| 53 | `53.jpg` | `DL1MR0230` | 65.17 | Crop (50-200ms) |
| 54 | `54.jpg` | `DL1NA0230` | 61.27 | Crop (50-200ms) |
| 55 | `55.jpg` | `DL1NA0230` | 191.57 | Crop (50-200ms) |
| 56 | `56.jpg` | `DL1MA0230` | 60.80 | Crop (50-200ms) |
| 57 | `57.jpg` | `RJ11GC1682` | 61.86 | Crop (50-200ms) |
