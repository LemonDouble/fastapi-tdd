from app.models import Category
from tests.factories.models_factory import get_random_category_dict


def test_integrate_create_new_category_successful(client, db_session_integration):
    # Arrange : Prepare test data
    category_data = get_random_category_dict()
    category_data.pop("id")

    # Act
    response = client.post("api/category/", json=category_data)

    # Assert : Verify Response
    assert response.status_code == 201

    # Assert : Verify the Response and Database State
    created_category = (
        db_session_integration.query(Category)
        .filter_by(id=response.json()["id"])
        .first()
    )

    assert created_category is not None

    # Assert : Verify response data matches database entry
    assert response.json() == {
        column.name: getattr(created_category, column.name)
        for column in created_category.__table__.columns
    }


def test_integrate_create_new_category_duplicated(client, db_session_integration):
    category_data = get_random_category_dict()
    new_category = Category(**category_data)
    db_session_integration.add(new_category)
    db_session_integration.commit()

    category_data.pop("id")
    response = client.post("api/category/", json=category_data)

    assert response.status_code == 400
