import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.database import get_async_session

from app.schemas.order import OrderCreate, OrderResponse
from app.crud.order import create_order, get_order
from aiocache import cached

router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order_endpoint(
        order: OrderCreate,
        db: AsyncSession = Depends(get_async_session)
):

    return await create_order(db, order)


@router.get("/{order_uuid}")
@cached(ttl=60)
async def get_order_endpoint(
        order_uuid: uuid.UUID,
        db: AsyncSession = Depends(get_async_session)
):
    return await get_order(db, order_uuid)
