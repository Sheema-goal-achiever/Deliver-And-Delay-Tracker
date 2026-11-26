from datetime import datetime
from typing import Literal
from pydantic import BaseModel, field_validator, model_validator

ShipmentStatus = Literal[
    "CREATED",
    "PICKED_UP",
    "IN_TRANSIT",
    "CUSTOMS_HOLD",
    "DELIVERED",
    "DELAYED",
]


class User(BaseModel):
    user_id: int
    full_name: str
    email: str
    address: str
    created_at: datetime


class Shipments(BaseModel):
    shipment_id: int
    tracking_code: str
    user_id: int
    origin: str
    destination: str
    current_status: str
    promised_delivery_at: datetime
    delivered_at: datetime | None = None
    created_at: datetime

    @field_validator("current_status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        allowed_statuses = [
            "CREATED",
            "PICKED_UP",
            "IN_TRANSIT",
            "CUSTOMS_HOLD",
            "DELIVERED",
            "DELAYED",
        ]
        if value not in allowed_statuses:
            raise ValueError(
                f"Invalid status: {value}. Allowed statuses are: {allowed_statuses}"
            )
        return value

    @model_validator(mode="after")
    def validate_delivered_timestamp(self) -> "Shipments":
        if self.current_status == "DELIVERED" and self.delivered_at is None:
            raise ValueError(
                "delivered_at must be provided when current_status is 'DELIVERED'"
            )
        return self


class Shipments_events(BaseModel):
    event_id: int
    shipment_id: int
    idempotency_key: str
    status: str
    location: str
    occurred_at: datetime
    recorded_at: datetime

    @field_validator("status")
    @classmethod
    def validate_event_type(cls, value: str) -> str:
        allowed_event_types = [
            "CREATED",
            "PICKED_UP",
            "IN_TRANSIT",
            "CUSTOMS_HOLD",
            "DELIVERED",
            "DELAYED",
        ]
        if value not in allowed_event_types:
            raise ValueError(
                f"Invalid event type: {value}. Allowed event types are: {allowed_event_types}"
            )
        return value