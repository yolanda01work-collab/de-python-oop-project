import csv
import json
import psycopg2


class RejectedRecordWriter:

    def __init__(self, output_path):
        self.output_path = output_path

    def write(self, rejected_records):

        with open(
            self.output_path,
            "w",
            newline="",
            encoding="utf8"
        ) as file:

            fieldnames = [
                "order_id",
                "raw_record",
                "reason"
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            for record in rejected_records:

                writer.writerow(
                    {
                        "order_id": record.order_id,
                        "raw_record": json.dumps(
                            record.raw_record
                        ),
                        "reason": record.reason
                    }
                )



class DatabaseConnection:

    def __init__(
        self,
        host,
        port,
        database,
        user,
        password
    ):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None


    def connect(self):

        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

        return self.connection


    def commit(self):

        if self.connection:
            self.connection.commit()


    def rollback(self):

        if self.connection:
            self.connection.rollback()


    def close(self):

        if self.connection:
            self.connection.close()



class PostgresLoader:

    def __init__(self, connection):
        self.connection = connection


    def create_tables(self, schema_path):

        with open(
            schema_path,
            "r",
            encoding="utf8"
        ) as file:

            sql = file.read()

        cursor = self.connection.cursor()

        cursor.execute(sql)

        self.connection.commit()

        cursor.close()


    def load_customers(self, customers):

        cursor = self.connection.cursor()

        query = """
            INSERT INTO dim_customers (
                customer_id,
                customer_name,
                region
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (customer_id)
            DO NOTHING;
        """

        for customer in customers:

            cursor.execute(
                query,
                (
                    customer.customer_id,
                    customer.customer_name,
                    customer.region
                )
            )

        self.connection.commit()

        cursor.close()


    def load_products(self, products):

        cursor = self.connection.cursor()

        query = """
            INSERT INTO dim_products (
                product_id,
                product_name,
                category
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (product_id)
            DO NOTHING;
        """

        for product in products:

            cursor.execute(
                query,
                (
                    product.product_id,
                    product.product_name,
                    product.category
                )
            )

        self.connection.commit()

        cursor.close()


    def load_stg_sales(self, records):
        cursor = self.connection.cursor()

        query = """
            INSERT INTO stg_sales (
                order_id,
                order_date,
                customer_id,
                product_id,
                quantity,
                unit_price,
                discount_rate
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (order_id)
            DO NOTHING;
        """

        for record in records:

            cursor.execute(
                query,
                (
                    record.order_id,
                    record.order_date,
                    record.customer_id,
                    record.product_id,
                    record.quantity,
                    record.unit_price,
                    record.discount_rate
                )
           )

        self.connection.commit()

        cursor.close()


    def load_fact_sales(self, records):

        cursor = self.connection.cursor()

        query = """
            INSERT INTO fact_sales (
                order_id,
                order_date,
                customer_id,
                product_id,
                quantity,
                unit_price,
                discount_rate,
                gross_sales,
                discount_amount,
                net_sales
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            ON CONFLICT (order_id)
            DO NOTHING;
        """

        for record in records:

            cursor.execute(
                query,
                (
                    record.order_id,
                    record.order_date,
                    record.customer_id,
                    record.product_id,
                    record.quantity,
                    record.unit_price,
                    record.discount_rate,
                    record.gross_sales,
                    record.discount_amount,
                    record.net_sales
                )
            )

        self.connection.commit()

        cursor.close()


    def load_rejected_sales(self, rejected_records):

        cursor = self.connection.cursor()

        query = """
            INSERT INTO etl_rejected_sales (
                order_id,
                raw_record,
                reason
            )
            VALUES (
                %s, %s, %s
            );
        """

        for record in rejected_records:

            cursor.execute(
                query,
                (
                    record.order_id,
                    json.dumps(record.raw_record),
                    record.reason
                )
            )

        self.connection.commit()

        cursor.close()