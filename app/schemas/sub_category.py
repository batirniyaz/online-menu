import datetime

from pydantic import BaseModel, Field
from typing import Optional, List

from app.schemas.product import ProductResponse


class SubCategoryBase(BaseModel):
    name: str = Field(..., description="The name of the sub category")
    sort_order: int = Field(..., description="The sort order of the sub category")
    category_id: int = Field(..., description="The ID of the category the sub category is associated with")


class SubCategoryCreate(SubCategoryBase):
    pass


class SubCategoryUpdate(SubCategoryBase):
    name: Optional[str] = Field(None, description="The name of the sub category")
    sort_order: Optional[int] = Field(None, description="The sort order of the sub category")
    category_id: Optional[int] = Field(None, description="The ID of the category the sub category is associated with")


class SubCategoryResponse(SubCategoryBase):
    id: int = Field(..., description="The ID of the sub category")
    products: Optional[List[ProductResponse]] = Field([],
                                                      description="A list of products associated with the sub category")

    created_at: datetime.datetime = Field(..., description="The time the sub category was created")
    updated_at: datetime.datetime = Field(..., description="The time the sub category was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "First meal",
                "sort_order": 1,
                "category_id": 1,
                "products": ["Fruit", "Egg"]
            }
        }
