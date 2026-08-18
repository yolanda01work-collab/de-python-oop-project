from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Customer:
    customer_id: str
    customer_name: str
    region: str


@dataclass
class Product:
    product_id: str
    product_name: str
    category: str


@dataclass
class RawSalesRecord:
    order_id: str
    order_date: str
    customer_id: str
    product_id: str
    quantity: str
    unit_price: str
    discount_rate: str


@dataclass
class ValidSalesRecord:
    order_id: int
    order_date: str
    customer_id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    discount_rate: Decimal


@dataclass
class FactSalesRecord:
    order_id: int
    order_date: str
    customer_id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    discount_rate: Decimal
    gross_sales: Decimal
    discount_amount: Decimal
    net_sales: Decimal


@dataclass
class RejectedRecord:
    order_id: str
    raw_record: dict
    reason: str