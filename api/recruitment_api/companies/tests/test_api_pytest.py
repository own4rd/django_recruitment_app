import json
from typing import List
from urllib import response
import pytest
from django.urls import reverse

from companies.models.company import Company


companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db

# ---------------------- Test Get Companies ---------------------
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)

    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_companies_should_return_empty_list(client) -> None:
    test_company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("status") == "Contratando"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


@pytest.fixture
def amazon() -> Company:
    return Company.objects.create(name="amazon")


def test_one_company_exists_should_succeed(client, amazon) -> None:
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]

    assert response.status_code == 200
    assert response_content.get("name") == amazon.name
    assert response_content.get("status") == "Contratando"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


# ---------------------- Test Post Companies ---------------------
def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="apple")
    response = client.post(path=companies_url, data={"name": "apple"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this Nome already exists."]
    }


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "test company name"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "test company name"
    assert response_content.get("status") == "Contratando"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "test company name", "status": "Layoffs"}
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "Layoffs"


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "test company name", "status": "layoffs"}
    )
    assert response.status_code == 400
    assert "is not a valid choice" in str(response.content)


# -------------------- Fixtures --------------


@pytest.fixture
def companies(request, company):
    """
    request: This is a pytest request type
    """
    companies = []
    names = request.param
    for name in names:
        companies.append(company(name=name))

    return companies


@pytest.fixture
def company(**kwargs):
    def _company_factory(**kwargs) -> Company:
        company_name = kwargs.pop("name", "Test Company INC")
        return Company.objects.create(name=company_name, **kwargs)

    return _company_factory


def old_test_multiple_companies_exists_should_succeed(client, company) -> None:
    tiktok: Company = company(name="Tiktok")
    twitch: Company = company(name="Twitch")
    test_company: Company = company()
    company_names = {tiktok.name, twitch.name, test_company.name}
    response_companies = client.get(companies_url).json()
    assert len(company_names) == len(response_companies)
    response_company_names = set(
        map(lambda company: company.get("name"), response_companies)
    )

    assert company_names == response_company_names


# INDIRECT -> Pass values
@pytest.mark.parametrize(
    "companies",
    [["Tiktok", "Twitch", "Test Company"], ["Facebook", "Instagram"]],
    ids=["3 T Companies", "Zuck Companies"],
    indirect=True,
)
def test_multiple_companies_exists_should_succeed(client, companies) -> None:
    """
    Refactored multiple_companies_*
    """
    response_companies = client.get(companies_url).json()
    company_names = set(map(lambda x: x.name, companies))
    assert len(company_names) == len(response_companies)
    response_company_names = set(
        map(lambda company: company.get("name"), response_companies)
    )

    assert company_names == response_company_names
