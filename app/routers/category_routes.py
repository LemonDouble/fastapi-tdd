import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_connection import get_db_session
from app.models import Category
from app.schema.category_schema import CategoryReturn, CategoryCreate, CategoryUpdate
from app.utils.category_utils import check_existing_category

router = APIRouter()
logger = logging.getLogger(__name__)


@router.put(
    "/{category_id}", response_model=CategoryReturn, status_code=HTTPStatus.CREATED
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db_session),
):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Category does not exist"
            )
        for key, value in category_data.model_dump().items():
            setattr(category, key, value)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"unexpected error occurred while updating category: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/slug/{category_slug}", response_model=CategoryReturn)
def get_category_by_slug(category_slug: str, db: Session = Depends(get_db_session)):
    try:
        category = db.query(Category).filter(Category.slug == category_slug).first()
        if category is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Category does not exist"
            )
        return category
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"unexpected error occurred while creating category: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/", response_model=list[CategoryReturn])
def get_categories(db: Session = Depends(get_db_session)):
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        logger.error(f"unexpected error occurred while creating category: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=CategoryReturn, status_code=HTTPStatus.CREATED)
def create_category(
    category_data: CategoryCreate, db: Session = Depends(get_db_session)
):
    try:
        check_existing_category(db=db, category_data=category_data)
        new_category = Category(**category_data.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"unexpected error occurred while creating category: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
