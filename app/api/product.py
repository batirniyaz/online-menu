from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.database import get_async_session

from app.crud.product import create_product, get_products, get_product, update_product, delete_product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from fastapi_cache.decorator import cache

router = APIRouter()


@router.post("/", response_model=ProductResponse)
async def create_product_endpoint(
        name: str = Query(...),
        price: float = Query(...),
        description: str = Query(...),
        status: bool = Query(...),
        sort_order: int = Query(...),
        sub_category_id: int = Query(...),
        image: UploadFile = File(...),
        db: AsyncSession = Depends(get_async_session)
):
    product = ProductCreate(
        name=name,
        price=price,
        description=description,
        status=status,
        sort_order=sort_order,
        sub_category_id=sub_category_id
    )

    return await create_product(db, product, image)


@router.get("/")
@cache(expire=60)
async def get_products_endpoint(
        db: AsyncSession = Depends(get_async_session)
):
    return await get_products(db)


@router.get("/{product_id}")
@cache(expire=60)
async def get_product_endpoint(product_id: int, db: AsyncSession = Depends(get_async_session)):
    return await get_product(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(
        product_id: int,
        name: str = Query(None),
        price: float = Query(None),
        description: str = Query(None),
        status: bool = Query(None),
        sort_order: int = Query(None),
        sub_category_id: int = Query(None),
        image: UploadFile = File(None),
        db: AsyncSession = Depends(get_async_session)
):
    product = ProductUpdate(
        name=name,
        price=price,
        description=description,
        status=status,
        sort_order=sort_order,
        sub_category_id=sub_category_id
    )
    return await update_product(db, product_id, product, image)


@router.delete("/{product_id}")
async def delete_product_endpoint(product_id: int, db: AsyncSession = Depends(get_async_session)):
    return await delete_product(db, product_id)
