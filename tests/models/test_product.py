from sqlalchemy import Boolean, DateTime, Enum, Integer, String, Text, UUID


def test_model_structure_table_exists(db_inspector):
    """
    테이블이 존재하는지 확인
    """
    assert db_inspector.has_table("product")


def test_model_structure_column_data_types(db_inspector):
    """
    테이블에 있는 데이터 타입과 필드들이 정상적으로 존재하는지 확인
    """
    table = "product"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["pid"]["type"], UUID)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["description"]["type"], Text)
    assert isinstance(columns["is_digital"]["type"], Boolean)
    assert isinstance(columns["created_at"]["type"], DateTime)
    assert isinstance(columns["updated_at"]["type"], DateTime)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["stock_status"]["type"], Enum)
    assert isinstance(columns["category_id"]["type"], Integer)
    assert isinstance(columns["seasonal_id"]["type"], Integer)


def test_model_structure_nullable_constraints(db_inspector):
    """
    테이블의 Nullable, Non-Nullable 필드가 정상 설정되어 있는지 테스트
    """
    table = "product"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "pid": False,
        "name": False,
        "slug": False,
        "description": True,
        "is_digital": False,
        "created_at": False,
        "updated_at": False,
        "is_active": False,
        "stock_status": False,
        "category_id": False,
        "seasonal_id": True,
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
    table = "product"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "product_name_length_check" for constraint in constraints
    )
    assert any(
        constraint["name"] == "product_slug_length_check" for constraint in constraints
    )


def test_model_structure_default_values(db_inspector):
    """
    테이블의 Default Value가 정상 설정되어 있는지 테스트
    """
    table = "product"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["is_digital"]["default"] == "false"
    assert columns["is_active"]["default"] == "false"
    assert columns["stock_status"]["default"] == "'oos'::status_enum"  # Out Of Stock


def test_model_structure_column_lengths(db_inspector):
    """
    테이블의 길이 제한이 잘 적용되어 있는지 확인
    """

    table = "product"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 200
    assert columns["slug"]["type"].length == 220


def test_model_structure_unique_constraints(db_inspector):
    """
    테이블의 Unique Constrints가 잘 적용되어 있는지 확인
    """
    table = "product"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "uq_product_pid" for constraint in constraints)
    assert any(constraint["name"] == "uq_product_name" for constraint in constraints)
    assert any(constraint["name"] == "uq_product_slug" for constraint in constraints)


def test_model_structure_foreign_key(db_inspector):
    """
    테이블의 FK가 잘 설정되어 있는지 확인
    """
    table = "product"
    foreign_keys = db_inspector.get_foreign_keys(table)

    category_foreign_key = next(
        (fk for fk in foreign_keys if fk["constrained_columns"] == ["category_id"]),
        None,
    )
    seasonal_foreign_key = next(
        (fk for fk in foreign_keys if fk["constrained_columns"] == ["seasonal_id"]),
        None,
    )

    assert category_foreign_key is not None
    assert seasonal_foreign_key is not None
