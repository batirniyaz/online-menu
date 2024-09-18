from fastapi import HTTPException
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.order import Order
from app.schemas.order import OrderCreate
from app.crud.product import get_product
from app.crud.sub_category import get_sub_category
from app.crud.category import get_category


async def create_order(db: AsyncSession, order: OrderCreate):
    try:
        products = []
        for product in order.products:
            db_product = await get_product(db, product["product_id"])
            sub_category = await get_sub_category(db, db_product.sub_category_id)
            category = await get_category(db, sub_category.category_id)
            sub_category_dict = {
                "sub_category_id": sub_category.id,
                "sub_category_name": sub_category.name,
                "category_id": sub_category.category_id,
                "category_name": category.name,
            }
            products.append(
                {
                    "product_id": db_product.id,
                    "product_name": db_product.name,
                    "product_status": db_product.status,
                    "quantity": product["quantity"],
                    "price": db_product.price,
                    "sub_category": sub_category_dict,
                }
            )

        db_order = Order(**order.model_dump())
        db_order.products = products

        db.add(db_order)
        await db.commit()
        await db.refresh(db_order)

        return db_order
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_order(db: AsyncSession, order_uuid: uuid.UUID):
    result = await db.execute(select(Order).filter_by(uuid=order_uuid))
    order = result.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
