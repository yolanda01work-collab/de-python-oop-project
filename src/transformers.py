from src.models import Customer
from src.models import Product
from src.models import FactSalesRecord


class SalesDataTransformer:

    def transform_customers(self, raw_customers):

        customers = []

        for row in raw_customers:

            customer = Customer(
                customer_id=row["customer_id"],
                customer_name=row["customer_name"],
                region=row["region"]
            )

            customers.append(customer)

        return customers


    def transform_products(self, raw_products):

        products = []

        for row in raw_products:

            product = Product(
                product_id=row["product_id"],
                product_name=row["product_name"],
                category=row["category"]
            )

            products.append(product)

        return products


    def transform_sales(self, valid_records):

        fact_records = []

        for record in valid_records:

            gross_sales = (
                record.quantity
                * record.unit_price
            )

            discount_amount = (
                gross_sales
                * record.discount_rate
            )

            net_sales = gross_sales.__sub__(
                discount_amount
            )

            fact_record = FactSalesRecord(
                order_id=record.order_id,
                order_date=record.order_date,
                customer_id=record.customer_id,
                product_id=record.product_id,
                quantity=record.quantity,
                unit_price=record.unit_price,
                discount_rate=record.discount_rate,
                gross_sales=gross_sales,
                discount_amount=discount_amount,
                net_sales=net_sales
            )

            fact_records.append(fact_record)

        return fact_records