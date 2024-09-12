from app.models import Category
from tests.factories.models_factory import get_random_category_dict


def test_test(client, db_session_integration):
    category_data = get_random_category_dict()

    new_category = Category(**category_data)
    db_session_integration.add(new_category)
    db_session_integration.commit()
