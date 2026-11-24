
import io

import pytest

from app import app, allowed_file, recognize_image


@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        SECRET_KEY="temporary-test-key-not-for-production",
        WTF_CSRF_ENABLED=True,
    )
    with app.test_client() as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask Image Recognition Application" in response.data


def test_allowed_file():
    assert allowed_file("photo.jpg") is True
    assert allowed_file("photo.png") is True
    assert allowed_file("photo.txt") is False


def test_recognize_cat():
    assert recognize_image("my_cat.jpg") == "Cat"


def test_recognize_dog():
    assert recognize_image("my_dog.jpg") == "Dog"


def test_recognize_car():
    assert recognize_image("my_car.jpg") == "Car"


def test_recognize_unknown():
    assert recognize_image("flower.jpg") == "Unknown"


def test_predict_without_image(client):
    token_response = client.get("/csrf-token")
    assert token_response.status_code == 200

    token = token_response.json["csrf_token"]
    response = client.post(
        "/predict",
        headers={"X-CSRFToken": token},
    )

    assert response.status_code == 400
    assert response.json["error"] == "No image uploaded"


def test_predict_rejects_missing_csrf_token(client):
    response = client.post(
        "/predict",
        data={
            "image": (
                io.BytesIO(b"sample image content"),
                "cat.jpg",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400


def test_predict_with_valid_csrf_token(client):
    token_response = client.get("/csrf-token")
    token = token_response.json["csrf_token"]

    response = client.post(
        "/predict",
        data={
            "image": (
                io.BytesIO(b"sample image content"),
                "cat.jpg",
            )
        },
        headers={"X-CSRFToken": token},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.json["prediction"] == "Cat"
