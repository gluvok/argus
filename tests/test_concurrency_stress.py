import concurrent.futures
import io

from PIL import Image

from app.services.pipeline.orchestrator import recognize_plate_image


def test_concurrent_inference_thread_safety():
    img = Image.new("RGB", (640, 480), color=(200, 200, 200))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    jpeg_bytes = buf.getvalue()

    def run_inference(_):
        return recognize_plate_image(jpeg_bytes)

    # 10 parallel requests hitting pipeline simultaneously
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(run_inference, i) for i in range(10)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert len(results) == 10
    for res in results:
        assert hasattr(res, "results")
        assert isinstance(res.results, list)
        assert hasattr(res, "execution_time_ms")
