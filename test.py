import pytest

from app import add_numbers, app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --- Unit tests: the pure function, no HTTP involved ---

def test_add_numbers_integers():
    assert add_numbers(2, 3) == 5


def test_add_numbers_negative_and_decimal():
    assert add_numbers(-1.5, 0.5) == -1.0


# --- Route tests: real HTTP requests against the app, without a server ---

def test_index_returns_html_with_version(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello from the Jenkins pipeline!" in response.data
    assert b"Version:" in response.data


def test_health_reports_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_add_returns_sum(client):
    response = client.get("/api/add?a=2&b=3")
    assert response.status_code == 200
    assert response.get_json() == {"result": 5.0}


def test_add_missing_parameter_returns_400(client):
    response = client.get("/api/add?a=2")
    assert response.status_code == 400
    assert "required" in response.get_json()["error"]


def test_add_non_numeric_returns_400(client):
    response = client.get("/api/add?a=two&b=3")
    assert response.status_code == 400
    assert "numbers" in response.get_json()["error"]


def test_unknown_route_returns_404(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
