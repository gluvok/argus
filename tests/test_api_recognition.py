import os

from app.schemas import RecognitionResponse


def test_recognize_empty_file(client):
    response = client.post(
        "/recognize",
        files={"file": ("empty.jpg", b"", "image/jpeg")},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "empty" in data["message"].lower()


def test_recognize_invalid_image_bytes(client):
    response = client.post(
        "/recognize",
        files={"file": ("corrupt.jpg", b"not-a-valid-image-stream", "image/jpeg")},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False


def test_recognize_rejects_non_image_payload(client):
    response = client.post(
        "/recognize",
        files={"file": ("notes.txt", b"just some text", "text/plain")},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "could not decode" in data["message"].lower()


def test_recognize_sample_image(client, sample_image_bytes):
    response = client.post(
        "/recognize",
        files={"file": ("test.jpg", sample_image_bytes, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    validated = RecognitionResponse.model_validate(data)
    # Plain red box has no vehicle and no plate
    assert validated.results == []
    assert validated.execution_time_ms is not None


def test_recognize_real_image_if_present(client):
    image_path = os.path.join("tests", "images", "1.jpg")
    if not os.path.exists(image_path):
        return

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    response = client.post(
        "/recognize",
        files={"file": ("1.jpg", img_bytes, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    validated = RecognitionResponse.model_validate(data)
    assert isinstance(validated.results, list)
    if validated.results:
        assert validated.results[0].execution_time_ms > 0
    assert validated.execution_time_ms is not None


def test_recognize_rejects_spoofed_mime_type(client):
    # Spoof content type as image/jpeg but send text bytes
    response = client.post(
        "/recognize",
        files={"file": ("fake.jpg", b"not-a-real-jpeg", "image/jpeg")},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False


def test_recognize_accepts_valid_png(client, sample_png_bytes):
    response = client.post(
        "/recognize",
        files={"file": ("test.png", sample_png_bytes, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()
    validated = RecognitionResponse.model_validate(data)
    assert validated.execution_time_ms is not None
    assert isinstance(validated.results, list)
