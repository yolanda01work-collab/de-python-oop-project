from datetime import datetime
from decimal import Decimal, InvalidOperation

from src.models import ValidSalesRecord
from src.models import RejectedRecord


class SalesDataValidator:

    def validate(self, raw_records, customers, products):

        valid_records = []
        rejected_records = []

        customer_ids = {
            customer.customer_id
            for customer in customers
        }

        product_ids = {
            product.product_id
            for product in products
        }

        for row in raw_records:

            try:

                required_fields = [
                    "order_id",
                    "order_date",
                    "customer_id",
                    "product_id",
                    "quantity",
                    "unit_price",
                    "discount_rate"
                ]

                for field in required_fields:
                    if not row.get(field):
                        raise ValueError(
                            f"Missing required field: {field}"
                        )

                order_id = int(row["order_id"])
                quantity = int(row["quantity"])

                try:
                    datetime.strptime(
                        row["order_date"],
                        "%Y-%m-%d"
                    )
                except ValueError:
                    raise ValueError(
                        "Invalid order_date format"
                    )

                try:
                    unit_price = Decimal(
                        row["unit_price"]
                    )

                    discount_rate = Decimal(
                        row["discount_rate"]
                    )

                except InvalidOperation:
                    raise ValueError(
                        "Invalid numeric value"
                    )

                if quantity <= 0:
                    raise ValueError(
                        "Quantity must be greater than zero"
                    )

                if unit_price <= 0:
                    raise ValueError(
                        "Unit price must be greater than zero"
                    )

                if discount_rate < 0 or discount_rate > 1:
                    raise ValueError(
                        "Discount rate must be between 0 and 1"
                    )

                if row["customer_id"] not in customer_ids:
                    raise ValueError(
                        "Unknown customer ID"
                    )

                if row["product_id"] not in product_ids:
                    raise ValueError(
                        "Unknown product ID"
                    )

                valid_record = ValidSalesRecord(
                    order_id=order_id,
                    order_date=row["order_date"],
                    customer_id=row["customer_id"],
                    product_id=row["product_id"],
                    quantity=quantity,
                    unit_price=unit_price,
                    discount_rate=discount_rate
                )

                valid_records.append(valid_record)

            except ValueError as error:

                rejected_record = RejectedRecord(
                    order_id=row.get("order_id", ""),
                    raw_record=row,
                    reason=str(error)
                )

                rejected_records.append(
                    rejected_record
                )

        return valid_records, rejected_records