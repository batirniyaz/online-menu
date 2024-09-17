import datetime

from pydantic import BaseModel, Field
from typing import Optional, List

from app.schemas.sub_category import SubCategoryResponse


class CategoryBase(BaseModel):
    name: str = Field(..., description="The name of the category")
    sort_order: int = Field(..., description="The sort order of the category")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, description="The name of the category")
    sort_order: Optional[int] = Field(None, description="The sort order of the category")


class CategoryResponse(CategoryBase):
    id: int = Field(..., description="The ID of the category")
    sub_categories: Optional[List[SubCategoryResponse]] = Field([],
                                                                description="A list of sub categories associated with the category")

    created_at: datetime.datetime = Field(..., description="The time the category was created")
    updated_at: datetime.datetime = Field(..., description="The time the category was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Kitchen",
                "sort_order": 1,
                "sub_categories": ["First meal", "Second meal"]
            }
        }
