from fastapi import HTTPException
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.order import Order
from app.schemas.order import OrderCreate
from app.crud.product import get_product
from app.crud.sub_category import get_sub_category
from app.crud.category import get_category
from app.crud.option import get_option


async def create_order(db: AsyncSession, order: OrderCreate):
    try:
        products = []
        db_option = None
        for product in order.products:
            if product["product_id"] is not None:
                db_product = await get_product(db, product["product_id"])
            else:
                db_option = await get_option(db, product["option_id"])
                db_product = await get_product(db, db_option.product_id)

            sub_category = await get_sub_category(db, db_product.sub_category_id)
            category = await get_category(db, sub_category.category_id)

            if product["product_id"] is not None:

                additional_info = {
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
                        "additional_info": additional_info,
                    }
                )
            else:
                additional_info = {
                    "product_id": db_product.id,
                    "product_name": db_product.name,
                    "sub_category_id": sub_category.id,
                    "sub_category_name": sub_category.name,
                    "category_id": category.id,
                    "category_name": category.name,
                }
                products.append(
                    {
                        "option_id": db_option.id,
                        "option_name": db_option.name,
                        "quantity": product["quantity"],
                        "price": db_option.price,
                        "additional_info": additional_info,
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
