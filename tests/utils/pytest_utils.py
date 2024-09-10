import pytest


def pytest_collection_modifyitems(items):
    """
    pytest 테스트 이름을 읽어
    model이 있으면 model 마커를,
    structure가 있으면 structure 마커를 추가해 줌
    """
    for item in items:
        if "model" in item.name:
            item.add_marker(pytest.mark.model)
        if "structure" in item.name:
            item.add_marker(pytest.mark.model_structure)
        if "unit" in item.name:
            item.add_marker(pytest.mark.unit)
        if "unit_schema" in item.name:
            item.add_marker(pytest.mark.unit_schema)
