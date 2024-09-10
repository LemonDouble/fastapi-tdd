from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Category
from app.schema.category_schema import CategoryCreate


def check_existing_category(db: Session, category_data: CategoryCreate):
    existing_category = (
        db.query(Category)
        .filter(
            (Category.slug == category_data.slug)
            | (Category.name == category_data.name)
            & (Category.level == category_data.level)
        )
        .first()
    )

    if existing_category:
        if (
            existing_category.name == category_data.name
            and existing_category.level == category_data.level
        ):
            detailed_message = "Category with this name and level exists"
        else:
            detailed_message = "Category with this slug exists"

        raise HTTPException(status_code=400, detail=detailed_message)
