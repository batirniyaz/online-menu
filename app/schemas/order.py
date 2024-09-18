import datetime
from uuid import uuid4 as generate_uuid

from pydantic import BaseModel, Field
from typing import List, Dict
import uuid as uuid_module


class OrderCreate(BaseModel):
    products: List[Dict] = Field([
        {"product_id": 3 or None, "option_id": 2 or None, "quantity": 4},
        {"product_id": 4 or None, "option_id": 2 or None, "quantity": 3}],
        description="The products of the order")


class OrderResponse(OrderCreate):
    id: int = Field(..., description="The ID of the order")
    uuid: uuid_module.UUID = Field(..., description="The UUID of the order")

    created_at: datetime.datetime = Field(..., description="The time the order was created")
    updated_at: datetime.datetime = Field(..., description="The time the order was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "products": [{"product_id": 1, "option_id": 2, "quantity": 1}],
                "created_at": "2022-01-01T12:00:00",
                "updated_at": "2022-01-01T12:00:00"
            }
        }

