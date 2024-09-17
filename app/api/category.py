from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.category import (
    create_category,
    get_categories,
    update_category,
    delete_category,
    get_category
)
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.auth.database import get_async_session

router = APIRouter()


@router.post("/", response_model=CategoryResponse)
async def create_category_endpoint(category: CategoryCreate, db: AsyncSession = Depends(get_async_session)):

    return await create_category(db, category)


@router.get("/")
async def get_categories_endpoint(db: AsyncSession = Depends(get_async_session)):

    return await get_categories(db)


@router.get("/{category_id}")
async def get_category_endpoint(category_id: int, db: AsyncSession = Depends(get_async_session)):

    return await get_category(db, category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category_endpoint(
        category_id: int,
        category: CategoryUpdate,
        db: AsyncSession = Depends(get_async_session)):

    return await update_category(db, category_id, category)


@router.delete("/{category_id}")
async def delete_category_endpoint(category_id: int, db: AsyncSession = Depends(get_async_session)):

    return await delete_category(db, category_id)
