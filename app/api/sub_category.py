from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sub_category import (
    create_sub_category,
    get_sub_categories,
    get_sub_category,
    update_sub_category,
    delete_sub_category
)

from app.auth.database import get_async_session
from app.schemas.sub_category import SubCategoryCreate, SubCategoryResponse, SubCategoryUpdate
from fastapi_cache.decorator import cache

router = APIRouter()


@router.post("/", response_model=SubCategoryResponse)
async def create_sub_category_endpoint(
        sub_category: SubCategoryCreate,
        db: AsyncSession = Depends(get_async_session)
):
    return await create_sub_category(db, sub_category)


@router.get("/")
@cache(expire=60)
async def get_sub_categories_endpoint(
        db: AsyncSession = Depends(get_async_session)
):
    return await get_sub_categories(db)


@router.get("/{sub_category_id}")
@cache(expire=60)
async def get_sub_category_endpoint(
        sub_category_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    return await get_sub_category(db, sub_category_id)


@router.put("/{sub_category_id}", response_model=SubCategoryResponse)
async def update_sub_category_endpoint(
        sub_category_id: int,
        sub_category: SubCategoryUpdate,
        db: AsyncSession = Depends(get_async_session)
):
    return await update_sub_category(db, sub_category_id, sub_category)


@router.delete("/{sub_category_id}")
async def delete_sub_category_endpoint(
        sub_category_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    return await delete_sub_category(db, sub_category_id)
