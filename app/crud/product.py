from fastapi import HTTPException, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.utils.file_utils import save_upload_file
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.config import BASE_URL


async def create_product(db: AsyncSession, product: ProductCreate, image: UploadFile):
    try:

        main_image_url, file_path = save_upload_file(image)
        image_url = f"{main_image_url}{file_path}"

        db_product = Product(**product.model_dump(), image=image_url, options=[])

        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)

        db_product.image = f"{BASE_URL}{db_product.image}"

        return db_product
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    products = result.scalars().all()

    if not products:
        raise HTTPException(status_code=404, detail="Products not found")

    for product in products:
        product.image = f"{BASE_URL}{product.image}"

    return products


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).filter_by(id=product_id))
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.image = f"{BASE_URL}{product.image}"

    return product


async def update_product(db: AsyncSession, product_id: int, product: ProductUpdate, image: UploadFile):
    db_product = await get_product(db, product_id)

    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    BASE_URL, main_image_url, file_path = save_upload_file(image)

    if image:
        image_url = f"{main_image_url}{file_path}"
        db_product.image = image_url

    await db.commit()
    await db.refresh(db_product)

    db_product.image = f"{BASE_URL}{db_product.image}"

    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product(db, product_id)

    if db_product.options:
        raise HTTPException(status_code=400, detail="Product has options. Please delete them first.")

    await db.delete(db_product)
    await db.commit()

    return {"message": "Product deleted successfully."}