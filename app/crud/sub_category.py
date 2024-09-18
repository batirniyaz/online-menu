from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.category import Category

from app.models.sub_category import SubCategory
from app.schemas.sub_category import SubCategoryCreate, SubCategoryUpdate
from app.crud.category import get_category


async def create_sub_category(db: AsyncSession, sub_category: SubCategoryCreate):
    try:
        db_sub_category = SubCategory(**sub_category.model_dump(), products=[])
        res = await db.execute(select(Category).filter_by(id=sub_category.category_id))
        category = res.scalars().first()

        if not category:
            raise HTTPException(status_code=404, detail="Category for this sub_category not found")

        db.add(db_sub_category)
        await db.commit()
        await db.refresh(db_sub_category)

        return db_sub_category
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_sub_categories(db: AsyncSession):
    result = await db.execute(select(SubCategory))
    sub_categories = result.scalars().all()

    return sub_categories


async def get_sub_category(db: AsyncSession, sub_category_id: int):
    result = await db.execute(select(SubCategory).filter_by(id=sub_category_id))
    sub_category = result.scalars().first()

    if not sub_category:
        raise HTTPException(status_code=404, detail="SubCategory not found")

    return sub_category


async def update_sub_category(db: AsyncSession, sub_category_id: int, sub_category: SubCategoryUpdate):
    try:
        db_sub_category = await get_sub_category(db, sub_category_id)
        db_category = await get_category(db, sub_category.category_id)

        for key, value in sub_category.model_dump().items():
            setattr(db_sub_category, key, value)

        await db.commit()
        await db.refresh(db_sub_category)

        return db_sub_category
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_sub_category(db: AsyncSession, sub_category_id: int):
    try:
        db_sub_category = await get_sub_category(db, sub_category_id)

        if db_sub_category.products:
            raise HTTPException(status_code=400, detail="SubCategory has products, please remove them")

        await db.delete(db_sub_category)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "SubCategory deleted successfully"}
