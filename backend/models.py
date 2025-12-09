from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class OrderStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    COMPLETED = "completed"


class DriverStatus(str, Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    DELIVERING = "delivering"
    ON_BREAK = "on_break"
    OFFLINE = "offline"


@dataclass
class Location:
    lat: float
    lng: float


@dataclass
class Order:
    id: str
    customer: str
    pickup: Location
    dropoff: Location
    priority: str = "standard"
    status: OrderStatus = OrderStatus.PENDING
    assigned_driver_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Driver:
    id: str
    name: str
    vehicle_type: str
    status: DriverStatus = DriverStatus.AVAILABLE
    capacity: int = 5
    current_load: int = 0
    location: Location = field(default_factory=lambda: Location(33.6844, 73.0479))
    rating: float = 5.0
