from src.extractors import CSVExtractor
from src.extractors import JSONExtractor

from src.transformers import SalesDataTransformer

from src.validators import SalesDataValidator

from src.loaders import RejectedRecordWriter
from src.loaders import DatabaseConnection
from src.loaders import PostgresLoader


class SalesPipeline:

    def __init__(self):

        self.sales_path = (
            "data/raw/sales_2026_01.csv"
        )

        self.customer_path = (
            "data/raw/customers.json"
        )

        self.product_path = (
            "data/raw/products.json"
        )


    def run(self, dry_run=False):

        print("Starting sales pipeline")


        sales = CSVExtractor(
            self.sales_path
        ).extract()

        raw_customers = JSONExtractor(
            self.customer_path
        ).extract()

        raw_products = JSONExtractor(
            self.product_path
        ).extract()


        transformer = SalesDataTransformer()

        customers = transformer.transform_customers(
            raw_customers
        )

        products = transformer.transform_products(
            raw_products
        )


        validator = SalesDataValidator()

        valid_records, rejected_records = (
            validator.validate(
                sales,
                customers,
                products
            )
        )


        fact_records = transformer.transform_sales(
            valid_records
        )


        rejected_writer = RejectedRecordWriter(
            "data/rejected/rejected_sales.csv"
        )

        rejected_writer.write(
            rejected_records
        )


        print(
            "Total records:",
            len(sales)
        )

        print(
            "Valid records:",
            len(valid_records)
        )

        print(
            "Rejected records:",
            len(rejected_records)
        )


        if not dry_run:

            database = DatabaseConnection(
                host="127.0.0.1",
                port=5433,
                database="sales_database",
                user="postgres",
                password="postgres"
            )

            connection = database.connect()

            loader = PostgresLoader(
                connection
            )

            loader.create_tables(
                "sql/schema.sql"
            )

            loader.load_customers(
                customers
            )

            loader.load_products(
                products
            )

            loader.load_stg_sales(
                valid_records
            )

            loader.load_fact_sales(
                fact_records
            )

            loader.load_rejected_sales(
                rejected_records
            )

            database.close()


        return {
            "total_records": len(sales),
            "valid_records": len(valid_records),
            "rejected_records": len(rejected_records)
        }