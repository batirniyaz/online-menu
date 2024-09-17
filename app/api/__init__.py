from fastapi import APIRouter

from app.api.category import router as category_router
from app.api.sub_category import router as sub_category_router
from app.api.product import router as product_router
from app.api.option import router as option_router
from app.api.order import router as order_router
router = APIRouter()

router.include_router(order_router, prefix="/order", tags=["Order"])
router.include_router(category_router, prefix="/category", tags=["Category"])
router.include_router(sub_category_router, prefix="/sub_category", tags=["Sub Category"])
router.include_router(product_router, prefix="/product", tags=["Product"])
router.include_router(option_router, prefix="/option", tags=["Option"])
