# Argus — ANPR Microservice

Automatic Number Plate Recognition (ANPR) microservice designed for weighbridge gatekeeping. Features a **4-tier cascaded execution pipeline** combining **Fast-ALPR (YOLOv9-s + CCT-XS OCR with margin expansion)** as the primary engine with automatic fallback to **Argus's RapidOCR pipeline**, delivering thin, high-speed response schemas.

---

## 🚀 How to Run

### 1. Local Development

```bash
# Install dependencies
uv sync

# Run development server (hot-reload)
uv run fastapi dev

# Or run in production mode locally
uv run fastapi run --host 127.0.0.1
```

Interactive documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

### 2. Remote Pi Deployment (1-Command)

Compiles `app` with Nuitka into a native C extension (`app.*.so`), syncs model weights (`yolo26n.onnx`), purges all `.py` source files from client hardware, and configures systemd (`argus.service`) bound to `127.0.0.1:8000` with auto-restart on boot:

```bash
# Preview deployment commands locally (dry-run)
uv run python scripts/deploy.py --dry-run

# Deploy to Raspberry Pi 5
uv run python scripts/deploy.py --host gluvok@hermes.local
```

---

## ⚡ 4-Tier Cascaded Execution Pipeline

Argus uses a vehicle-first cascade. It first executes Stage 1 vehicle detection (YOLO26 ONNX Runtime CPU via `yolo26n.onnx`) and sorts vehicles by proximity:

1. **Tier 1 (Fast-ALPR on Vehicle Crops)**: Runs Fast-ALPR (YOLOv9-s plate detector + CCT-XS OCR with margin expansion) on extracted vehicle crops (`~30–50 ms`). Early exit if valid plate found.
2. **Tier 2 (Fast-ALPR Full-Frame Fallback)**: If vehicle crops yield no plates or zero vehicles were detected (e.g. non-COCO vehicles like tractors), runs Fast-ALPR across the entire image frame (`~30–50 ms`). Early exit if valid plate found.
3. **Tier 3 (RapidOCR on Vehicle Crops)**: If Fast-ALPR passes yield no valid plates, executes RapidOCR 2D spatial candidate pairing on vehicle crops (`~120–180 ms`). Early exit if valid plate found.
4. **Tier 4 (RapidOCR Full-Frame Fallback)**: If Tier 3 produces no plates or zero vehicles were detected, runs RapidOCR across the full image frame (`~220–280 ms`).

---

## 📡 API Reference

### `POST /recognize`

Recognize vehicle license plates from an uploaded image.

#### Request

Accepts a multipart file upload (`file`, up to 8 MB; supported: JPEG, PNG, WebP, BMP):

```bash
curl -X POST "http://127.0.0.1:8000/recognize" \
  -H "Accept: application/json" \
  -F "file=@tests/images/1.jpg"
```

#### Response (`200 OK`)

```json
{
  "results": [
    {
      "plate": "RJ09GA0165",
      "vehicle_box": [10, 10, 50, 50],
      "execution_time_ms": 31.42
    }
  ],
  "execution_time_ms": 31.42
}
```

- **`results`**: List of validated plate items.
  - **`plate`**: Normalized Indian vehicle registration number (e.g. `RJ09GA0165`).
  - **`vehicle_box`**: Vehicle bounding box `[x1, y1, x2, y2]` in image coordinates, or `null` if detected via full-frame fallback.
  - **`execution_time_ms`**: Item processing duration in milliseconds.
- **`execution_time_ms`**: Total end-to-end processing latency in milliseconds.

---

### `GET /health`

Health check endpoint confirming operational readiness.

```bash
curl -X GET "http://127.0.0.1:8000/health"
```

```json
{
  "status": "healthy",
  "service": "Argus ANPR Microservice",
  "version": "0.1.0"
}
```

---

### `GET /`

Root service information and documentation links.

```bash
curl -X GET "http://127.0.0.1:8000/"
```

```json
{
  "name": "Argus ANPR Microservice",
  "version": "0.1.0",
  "status": "running",
  "docs": "/docs"
}
```
