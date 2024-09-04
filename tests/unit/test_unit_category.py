import pytest
from pydantic import ValidationError

from app.schema.category_schema import CategoryCreate


def test_unit_schema_category_validation():
    valid_data = {"name": "test category", "slug": "test-slug"}
    category = CategoryCreate(**valid_data)

    assert category.name == "test category"
    assert category.slug == "test-slug"
    assert category.level == 100
    assert category.is_active is False
    assert category.parent_id is None

    invalid_data = {"name": "test category"} # Slug Missing

    with pytest.raises(ValidationError):
        category = CategoryCreate(**invalid_data)
