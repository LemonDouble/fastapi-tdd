import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_connection import get_db_session
from app.models import Category
from app.schema.category_schema import CategoryReturn, CategoryCreate
from app.utils.category_utils import check_existing_category

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=CategoryReturn, status_code=HTTPStatus.CREATED)
def create_category(category_data : CategoryCreate, db : Session =  Depends(get_db_session)):


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