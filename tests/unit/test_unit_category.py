import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models import Category
from app.schema.category_schema import CategoryCreate
from tests.factories.models_factory import get_random_category_dict


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value


def test_unit_schema_category_validation():
    """
    스키마가 Valid한 경우와 Invalid한 경우에 대해 스키마 테스트
    """
    valid_data = {"name": "test category", "slug": "test-slug"}
    category = CategoryCreate(**valid_data)

    assert category.name == "test category"
    assert category.slug == "test-slug"
    assert category.level == 100
    assert category.is_active is False
    assert category.parent_id is None

    invalid_data = {"name": "test category"}  # Slug Missing

    with pytest.raises(ValidationError):
        CategoryCreate(**invalid_data)


def test_unit_create_new_category_successfully(client, monkeypatch):
    """
    Valid한 데이터의 경우 카테고리 생성 성공 테스트
    """
    category = get_random_category_dict()

    for key, value in category.items():
        monkeypatch.setattr(Category, key, value)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    body = category.copy()
    body.pop("id")
    response = client.post("api/category", json=body)

    assert response.status_code == 201
    assert response.json() == category


@pytest.mark.parametrize(
    "existing_category, category_data, expected_detail",
    [
        (True, get_random_category_dict(), "Category with this name and level exists"),
        (True, get_random_category_dict(), "Category with this slug exists"),
    ],
)
def test_unit_create_new_category_existing(
    client, monkeypatch, existing_category, category_data, expected_detail
):
    """
    중복 데이터가 있는 경우 Exception 발생 테스트
    """

    def mock_check_existing_category(db, category_data):
        if existing_category:
            raise HTTPException(status_code=400, detail=expected_detail)

    monkeypatch.setattr(
        "app.routers.category_routes.check_existing_category",
        mock_check_existing_category,
    )
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())

    body = category_data.copy()
    body.pop("id")
    response = client.post("api/category", json=body)

    assert response.status_code == 400

    if expected_detail:
        assert response.json() == {"detail": expected_detail}


def test_unit_create_new_category_with_internal_server_error(client, monkeypatch):
    """
    DB 에러 등으로 예상치 못한 에러 발생시, 정상적으로 에러 핸들링하는지 테스트
    """
    category = get_random_category_dict()

    def mock_create_category_exception(*args, **kwargs):
        raise Exception("Internal Server Error")

    for key, value in category.items():
        monkeypatch.setattr(Category, key, value)
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_create_category_exception)

    body = category.copy()
    body.pop("id")
    response = client.post("api/category", json=body)

    assert response.status_code == 500
