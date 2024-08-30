from sqlalchemy import Boolean, Integer, String


def test_model_structure_table_exists(db_inspector):
    """
    테이블이 존재하는지 확인
    """
    assert db_inspector.has_table("category")


def test_model_structure_column_data_types(db_inspector):
    """
    테이블에 있는 데이터 타입과 필드들이 정상적으로 존재하는지 확인
    """
    table = "category"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["level"]["type"], Integer)
    assert isinstance(columns["parent_id"]["type"], Integer)


def test_model_structure_nullable_constraints(db_inspector):
    """
    테이블의 Nullable, Non-Nullable 필드가 정상 설정되어 있는지 테스트
    """
    table = "category"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id":        False,
        "name":      False,
        "slug":      False,
        "is_active": False,
        "level":     False,
        "parent_id": True,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(column_name), f"column {column_name} is not as null expected"


def test_model_structure_column_constraints(db_inspector):
    """
    테이블의 Constraints 설정이 정상 설정되어 있는지 테스트
    """
    table = "category"
    constraints = db_inspector.get_check_constraints(table)

    assert any(constraint["name"] == "category_name_length_check" for constraint in constraints)
    assert any(constraint["name"] == "category_slug_length_check" for constraint in constraints)


def test_model_structure_default_values(db_inspector):
    """
    테이블의 Default Value가 정상 설정되어 있는지 테스트
    """
    table = "category"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["is_active"]["default"] == "false"
    assert columns["level"]["default"] == "100"


def test_model_structure_column_lengths(db_inspector):
    """
    테이블의 길이 제한이 잘 적용되어 있는지 확인
    """

    table = "category"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 100
    assert columns["slug"]["type"].length == 120


def test_model_structure_unique_constraints(db_inspector):
    """
    테이블의 Unique Constrints가 잘 적용되어 있는지 확인
    """
    table = "category"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "uq_category_name_level" for constraint in constraints)
    assert any(constraint["name"] == "uq_category_slug" for constraint in constraints)


def test_model_structure_foreign_key(db_inspector):
    """
    테이블의 FK가 잘 설정되어 있는지 확인
    """
    table = "category"
    foreign_keys = db_inspector.get_foreign_keys(table)

    parent_foreign_key = next((fk for fk in foreign_keys if fk["constrained_columns"] == ["parent_id"]), None)

    assert parent_foreign_key is not None
