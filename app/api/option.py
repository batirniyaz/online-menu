from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.database import get_async_session

from app.schemas.option import OptionCreate, OptionResponse, OptionUpdate
from app.crud.option import create_option, get_options, update_option, get_option, delete_option

router = APIRouter()


@router.post("/", response_model=OptionResponse)
async def create_option_endpoint(
        option: OptionCreate,
        db: AsyncSession = Depends(get_async_session)
):

    return await create_option(db, option)


@router.get("/", )
async def get_options_endpoint(
        db: AsyncSession = Depends(get_async_session)
):
    return await get_options(db)


@router.get("/{option_id}")
async def get_option_endpoint(
        option_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    return await get_option(db, option_id)


@router.put("/{option_id}", response_model=OptionResponse)
async def update_option_endpoint(
        option_id: int,
        option: OptionUpdate,
        db: AsyncSession = Depends(get_async_session)
):
    return await update_option(db, option_id, option)


@router.delete("/{option_id}")
async def delete_option_endpoint(
        option_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    return await delete_option(db, option_id)
