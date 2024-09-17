from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.config import BASE_URL


async def create_category(db: AsyncSession, category: CategoryCreate):
    try:
        db_category = Category(**category.model_dump(), sub_categories=[])
        db.add(db_category)
        await db.commit()
        await db.refresh(db_category)

        return db_category
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    categories = result.scalars().all()

    for category in categories:
        for sub_category in category.sub_categories:
            for product in sub_category.products:
                product.image = f"{BASE_URL}{product.image}"

    return categories


async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(Category).filter_by(id=category_id))
    db_category = result.scalars().first()

    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    products = []
    for sub_category in db_category.sub_categories:
        for product in sub_category.products:
            product.image = f"{BASE_URL}{product.image}"
            products.append(product)

    db_category.products = products
    return db_category


async def update_category(db: AsyncSession, category_id: int, category: CategoryUpdate):
    result = await db.execute(select(Category).filter_by(id=category_id))
    db_category = result.scalars().first()

    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)

    await db.commit()
    await db.refresh(db_category)

    return db_category


async def delete_category(db: AsyncSession, category_id: int):
    db_category = await get_category(db, category_id)

    if db_category.sub_categories:
        raise HTTPException(status_code=400, detail="sub-categories of category is not empty")

    await db.delete(db_category)
    await db.commit()
    return {"message": "Category deleted successfully"}


