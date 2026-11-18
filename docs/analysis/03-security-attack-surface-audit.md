# 03 - Security & Input Boundary Attack Surface Audit

## 1. Unbounded Upload Memory Buffering (DoS Risk)

- **Location**: `app/api/routes/recognition.py:22`
- **Issue**:
  ```python
  image_bytes = await file.read()
  validate_image_upload(image_bytes, content_type=file.content_type)
  ```
  `await file.read()` reads the entire incoming payload into server memory before `validate_image_upload()` checks `MAX_UPLOAD_BYTES` (8 MB).
- **Vulnerability**: A malicious client transmitting a large stream (e.g. 2 GB) causes the FastAPI/Uvicorn process to buffer the full payload in RAM. On hardware with constrained memory (Raspberry Pi 5 with 4–8 GB RAM sharing memory with inference engines), concurrent large uploads will trigger Linux kernel OOM killing of `argus.service`.
- **Remediation**: Read incoming `file` in fixed chunks (e.g. 64 KB) with an accumulator; raise `PayloadTooLargeError` immediately once total bytes exceed `MAX_UPLOAD_BYTES`.

---

## 2. Insecure / Invalid CORS Header Combination

- **Location**: `app/core/constants.py:16-17` & `app/core/middleware.py:15-21`
- **Issue**:
  ```python
  CORS_ORIGINS: list[str] = ["*"]
  CORS_ALLOW_CREDENTIALS = True
  ```
- **Vulnerability**: Per W3C Fetch specification and OWASP API security standards, the header `Access-Control-Allow-Origin: *` cannot be combined with `Access-Control-Allow-Credentials: true`. Browsers automatically reject and drop responses containing this combination.
- **Remediation**: For an edge weighbridge microservice, set `CORS_ALLOW_CREDENTIALS = False` when using wildcard origins, or require explicit allowed origins (e.g., `["http://localhost:3000", "http://127.0.0.1:8000"]`) when credentials are required.

---

## 3. Pixel Budget Guard Lifecycle Leak

- **Location**: `app/services/image_processing/loader.py:14` vs `app/services/image_processing/security.py:25`
- **Issue**:
  `Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS` (50 MP) is assigned as a side-effect of importing `loader.py`. However, incoming requests execute `probe_image()` in `security.py` before `loader.py` is imported. Until `loader.py` is imported, Pillow defaults to ~89.5 MP rather than the configured 50 MP threshold.
- **Remediation**: Set `Image.MAX_IMAGE_PIXELS` in `app/core/constants.py` or `security.py` immediately at module load time.

---

## 4. Deployment Command Shell Pipe Execution

- **Location**: `scripts/deploy_commands.py:18`
- **Issue**: Remote preparation command runs `curl -LsSf https://astral.sh/uv/install.sh | sh` over SSH on target hardware.
- **Remediation**: Pin uv installation or verify SHA-256 checksums if bootstrap integrity verification is needed on sensitive weighbridge networks.
