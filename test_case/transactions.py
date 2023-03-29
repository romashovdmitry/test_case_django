from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()


class SQLTransactions():

    password = os.getenv('DB_PASSWORD')
    name = os.getenv('DB_NAME')
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')

    db = create_engine(
        f'postgresql://{user}:{password}@{host}:5432/{name}')
    conn = db.connect()

    def __init__(self, city_code=None, number=None):

        self.city_code = city_code
        self.number = number

    def search_data(self):

        return (
            self.db.execute(
                "SELECT region.geo, operator "
                "FROM phone_number "
                "JOIN region "
                "ON phone_number.region_pk=region.region_pk "
                f"AND region.city_code={self.city_code} "
                "AND ("
                f"(start={self.number} OR finish={self.number})"
                f"OR (start<{self.number} AND finish>{self.number})"
                ");").first()
        )

    def delete_all_data(self):
        self.db.execute(
            "DELETE FROM phone_number;"
            "DELETE FROM region;"
            "DELETE FROM operator;"
        )
