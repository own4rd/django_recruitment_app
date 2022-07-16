import requests
import json
import pytest

test_env_companies_url = "http://127.0.0.1:8000/companies/"


def test_zero_companies_django_agnostic() -> None:
    response = requests.get(url=test_env_companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_create_company_with_layoffs_django_agnostic() -> None:
    response = requests.post(
        url=test_env_companies_url,
        data={"name": "test company name", "status": "Layoffs"},
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "Layoffs"

    cleanup_company(company_id=response_content["id"])


def cleanup_company(company_id: str) -> None:
    response = requests.delete(url=f"http://127.0.0.1:8000/companies/{company_id}")
    assert response.status_code == 204


# ---------------- API CRIPTO ------------

@pytest.mark.crypto
def test_dogecoin_api() -> None:
    response = requests.get(
        url="https://api.cryptonator.com/api/ticker/btc-usd",
        headers={'User-Agent': 'Chrome'}
    )

    assert response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content['ticker']['base'] == 'DOGE'

import responses
@pytest.mark.crypto
@responses.activate
def test_mocked_dogecoin_api() -> None:
    responses.add(method=responses.GET, url="https://api.cryptonator.com/api/ticker/btc-usd", json={
        "ticker": {
            "base": "EDEN",
            "target": "EDEN-USD",
            "price": "0.04535907",
            "volume": "0975940509.758770037",
            "change": "-0.00052372",
        },
        "timestamp": 1612515303,
        "success": True,
        "error": ""
    }, status=200)
    response = requests.get(
        url="https://api.cryptonator.com/api/ticker/btc-usd",
        headers={'User-Agent': 'Chrome'}
    )

    assert response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content['ticker']['base'] == 'EDEN'
    assert response_content['ticker']['target'] == 'EDEN-USD'
