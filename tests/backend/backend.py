from fastapi.testclient import TestClient
from jsonschema import validate

from backend.api import app

client = TestClient(app)


def test_api_health():
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"msg": "API is healthy"}


def test_get_cases_by_name():
    params = {"case_name": "rasul v. bush", "citation": None, "jurisdiction": None}
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "case_name": {"type": "string"},
                "citation": {"type": "string"},
                "id": {"type": "number"},
            },
        },
    }
    response = client.post("/cases/query_by_name", params=params)
    assert response.status_code == 200
    assert validate(response.json(), schema) is None


def test_get_case_by_name_and_citation():
    params = {
        "case_name": "hamdan v. rumsfeld",
        "citation": "543 U.S. 1019",
        "jurisdiction": None,
    }
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "case_name": {"type": "string"},
                "citation": {"type": "string"},
                "id": {"type": "number"},
            },
        },
    }
    response = client.post("/cases/query_by_name", params=params)
    assert response.status_code == 200
    assert validate(response.json(), schema) is None


def test_get_case_by_id():
    params = {"id": 5956288, "include_summary": False}
    schema = {
        "type": "object",
        "properties": {
            "case_name": {"type": "string"},
            "id": {"type": "number"},
            "short_title": {"type": "string"},
            "jurisdiction": {"type": "string"},
            "jurisdiction_id": {"type": "number"},
            "court": {"type": "string"},
            "court_id": {"type": "number"},
            "docket_number": {"type": "string"},
            "reporter_volume": {"type": "string"},
            "reporter": {"type": "string"},
            "reporter_id": {"type": "number"},
            "first_page": {"type": "string"},
            "date_decided": {"type": "string"},
            "citation": {"type": "string"},
            "case_type": {"type": "string"},
            "frontend_pdf_url": {"type": "string"},
            "summary": {"type": "null"},
        },
    }
    response = client.post("/cases/case", params=params)
    assert response.status_code == 200
    assert validate(response.json(), schema) is None


def test_get_case_by_id_with_summary():
    params = {"id": 5956288, "include_summary": True}
    schema = {
        "type": "object",
        "properties": {
            "case_name": {"type": "string"},
            "id": {"type": "number"},
            "short_title": {"type": "string"},
            "jurisdiction": {"type": "string"},
            "jurisdiction_id": {"type": "number"},
            "court": {"type": "string"},
            "court_id": {"type": "number"},
            "docket_number": {"type": "string"},
            "reporter_volume": {"type": "string"},
            "reporter": {"type": "string"},
            "reporter_id": {"type": "number"},
            "first_page": {"type": "string"},
            "date_decided": {"type": "string"},
            "citation": {"type": "string"},
            "case_type": {"type": "string"},
            "frontend_pdf_url": {"type": "string"},
            "summary": {"type": "string"},
        },
    }
    response = client.post("/cases/case", params=params)
    assert response.status_code == 200
    assert validate(response.json(), schema) is None


def test_get_case_summary():
    params = {"id": 12458787}
    schema = {"type": "string"}
    response = client.post("/cases/case/summary", params=params)
    assert response.status_code == 200
    assert validate(response.json(), schema) is None


def test_create_ris():
    params = {"id": 5930017}
    response = client.post("/cases/case/download", params=params)
    check_file = open("./tests/backend/resources/export.ris", "r")
    assert response.status_code == 200
    assert len(response.content) == 358
    assert response.text == check_file.read()
