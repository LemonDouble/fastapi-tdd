from sqlalchemy import DateTime, Integer, String


def test_model_structure_table_exists(db_inspector):
    """
    테이블이 존재하는지 확인
    """
    assert db_inspector.has_table("seasonal_event")


def test_model_structure_column_data_types(db_inspector):
    """
    테이블에 있는 데이터 타입과 필드들이 정상적으로 존재하는지 확인
    """
    table = "seasonal_event"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["start_date"]["type"], DateTime)
    assert isinstance(columns["end_date"]["type"], DateTime)
    assert isinstance(columns["name"]["type"], String)


def test_model_structure_nullable_constraints(db_inspector):
    """
    테이블의 Nullable, Non-Nullable 필드가 정상 설정되어 있는지 테스트
    """
    table = "seasonal_event"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "start_date": False,
        "end_date": False,
        "name": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column {column_name} is not as null expected"


def test_model_structure_column_constraints(db_inspector):
    """
    테이블의 Constraints 설정이 정상 설정되어 있는지 테스트
    """
    table = "seasonal_event"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "seasonal_event_name_length_check"
        for constraint in constraints
    )


def test_model_structure_unique_constraints(db_inspector):
    """
    테이블의 Unique Constrints가 잘 적용되어 있는지 확인
    """
    table = "seasonal_event"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_seasonal_event_name" for constraint in constraints
    )


def test_model_structure_column_lengths(db_inspector):
    """
    테이블의 길이 제한이 잘 적용되어 있는지 확인
    """

    table = "seasonal_event"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 100
