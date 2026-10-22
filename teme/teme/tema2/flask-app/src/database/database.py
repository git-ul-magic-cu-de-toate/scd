import pymysql
import logging
from typing import List, Tuple
from src.database.constants import (MYSQL_DB, MYSQL_HOST, MYSQL_PORT,
                                    MYSQL_PASSWORD, MYSQL_USER,
                                    UPDATE_COUNTRY_REQUEST,
                                    DELETE_COUNTRY_REQUEST,
                                    INSERT_CITY_REQUEST,
                                    UPDATE_CITY_REQUEST,
                                    DELETE_CITY_REQUEST,
                                    INSERT_TEMPERATURE_REQUEST,
                                    UPDATE_TEMPERATURE_REQUEST,
                                    DELETE_TEMPERATURE_REQUEST)
from src.utils import Country, City, Temperature, StatusCode

class DatabaseDriver():
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def get_all_countries(self) -> List[Country]:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        db_results = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, country_name, latitude, longitude FROM countries")
            db_results = cursor.fetchall()
        conn.close()

        if not db_results:
            return []
        
        results = []
        for db_result in db_results:
            if (db_result and db_result[0] and db_result[1]
                and db_result[2] and db_result[3]):
                results.append(
                    Country(
                        id=db_result[0],
                        name=db_result[1],
                        latitude=float(db_result[2]),
                        longitude=float(db_result[3])
                    )
                )
        
        return results
    
    def insert_new_country(self, name: str, latitude: float, longitude: float) -> int:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        country_id = -1
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO countries (country_name, latitude, longitude) VALUES (%s, %s, %s)",
                (name, str(latitude), str(longitude))
            )
            country_id = cursor.lastrowid
            conn.commit()

        except pymysql.IntegrityError:
            conn.rollback()

        finally:
            cursor.close()
            conn.close()

        return country_id

    def update_country_in_db(self, id: int, name: str, latitude: float, longitude: float) -> StatusCode:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        update_data_tuple = (
            name,
            latitude,
            longitude,
            id
        )

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM countries WHERE id = %s", (id,))
                result = cursor.fetchone()

                # country doesn't exist in database
                if result is None:
                    return StatusCode.NOT_FOUND

                cursor.execute(UPDATE_COUNTRY_REQUEST, update_data_tuple)

        except pymysql.IntegrityError:
            conn.rollback()
            return StatusCode.CONFLICT

        finally:
            conn.commit()
            conn.close()

        return StatusCode.SUCCESS
    
    def delete_country_from_db(self, id: int) -> StatusCode:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )


        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM countries WHERE id = %s", (id,))
            result = cursor.fetchone()

            # country doesn't exist in database
            if result is None:
                return StatusCode.NOT_FOUND

            cursor.execute(DELETE_COUNTRY_REQUEST, (id,))

        conn.commit()
        conn.close()

        return StatusCode.SUCCESS

    def get_all_cities(self) -> List[City]:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        db_results = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, country_id, city_name, latitude, longitude FROM cities")
            db_results = cursor.fetchall()
        conn.close()

        if not db_results:
            return []
        
        results = []
        for db_result in db_results:
            if (db_result and db_result[0] and db_result[1]
                and db_result[2] and db_result[3] and db_result[4]):
                results.append(
                    City(
                        id=db_result[0],
                        country_id=db_result[1],
                        name=db_result[2],
                        latitude=float(db_result[3]),
                        longitude=float(db_result[4])
                    )
                )
        
        return results

    def insert_new_city(self, country_id: int, name: str, latitude: float, longitude: float) -> Tuple[StatusCode, int]:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        city_id = -1
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM countries WHERE id = %s", (country_id,))
            result = cursor.fetchone()

            # country doesn't exist in database
            if result is None:
                return StatusCode.NOT_FOUND, -1

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    INSERT_CITY_REQUEST,
                    (country_id, name, str(latitude), str(longitude))
                )
                city_id = cursor.lastrowid

            conn.commit()

        except pymysql.IntegrityError:
            conn.rollback()
            return StatusCode.CONFLICT, city_id
        finally:
            cursor.close()
            conn.close()

        return StatusCode.CREATED, city_id

    def get_cities_for_country(self, country_id: int) -> List[City]:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        db_results = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, country_id, city_name, latitude, longitude FROM cities WHERE country_id = %s", (country_id,))
            db_results = cursor.fetchall()
        conn.close()

        if not db_results:
            return []
        
        results = []
        for db_result in db_results:
            if (db_result and db_result[0] and db_result[1]
                and db_result[2] and db_result[3] and db_result[4]):
                results.append(
                    City(
                        id=db_result[0],
                        country_id=db_result[1],
                        name=db_result[2],
                        latitude=float(db_result[3]),
                        longitude=float(db_result[4])
                    )
                )
        
        return results

    def update_city_in_db(self, id: int, country_id: int, name: str,
                             latitude: float, longitude: float) -> StatusCode:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        update_data_tuple = (
            name,
            latitude,
            longitude,
            id
        )

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cities WHERE id = %s", (id,))
                result = cursor.fetchone()

                # city doesn't exist in database
                if result is None:
                    return StatusCode.NOT_FOUND

                cursor.execute(UPDATE_CITY_REQUEST, update_data_tuple)

        except pymysql.IntegrityError:
            conn.rollback()
            return StatusCode.CONFLICT

        finally:
            conn.commit()
            conn.close()

        return StatusCode.SUCCESS

    def delete_city_from_db(self, id: int) -> StatusCode:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM cities WHERE id = %s", (id,))
            result = cursor.fetchone()

            # city doesn't exist in database
            if result is None:
                return StatusCode.NOT_FOUND

            cursor.execute(DELETE_CITY_REQUEST, (id,))

        conn.commit()
        conn.close()

        return StatusCode.SUCCESS
    
    def insert_new_temperature(self, city_id: int, value: float) -> Tuple[StatusCode, int]:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        temp_id = -1
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM cities WHERE id = %s", (city_id,))
            result = cursor.fetchone()

            # city doesn't exist in database
            if result is None:
                return StatusCode.NOT_FOUND, temp_id

        try:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_TEMPERATURE_REQUEST, (city_id, str(value)))
                temp_id = cursor.lastrowid

            conn.commit()

        except pymysql.IntegrityError:
            conn.rollback()
            return StatusCode.CONFLICT, temp_id
        finally:
            cursor.close()
            conn.close()

        return StatusCode.CREATED, temp_id

    def construct_query_temp_for_countries(self, latitude: float, longitude: float,
                                           date_from: str, date_until: str,
                                           country_id: int):
        conditions = []

        if latitude is not None:
            conditions.append(f"countries.latitude = {latitude}")

        if longitude is not None:
            conditions.append(f"countries.longitude = {longitude}")

        if date_from is not None:
            conditions.append(f"temperatures.tmp_timestamp >= '{date_from}'")

        if date_until is not None:
            conditions.append(f"temperatures.tmp_timestamp <= '{date_until}'")

        if country_id is not None:
            conditions.append(f"countries.id = {country_id}")

        query = """
            SELECT
                temperatures.id,
                temperatures.city_id,
                temperatures.tmp_value,
                temperatures.tmp_timestamp
            FROM
                temperatures
            JOIN
                cities ON temperatures.city_id = cities.id
            JOIN
                countries ON cities.country_id = countries.id
        """

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return query
    
    def construct_query_temp_for_cities(self, latitude: float, longitude: float,
                                           date_from: str, date_until: str,
                                           city_id: int):
        conditions = []

        if latitude is not None:
            conditions.append(f"cities.latitude = {latitude}")

        if longitude is not None:
            conditions.append(f"cities.longitude = {longitude}")

        if date_from is not None:
            conditions.append(f"temperatures.tmp_timestamp >= '{date_from}'")

        if date_until is not None:
            conditions.append(f"temperatures.tmp_timestamp <= '{date_until}'")

        if city_id is not None:
            conditions.append(f"cities.id = {city_id}")

        query = """
            SELECT
                temperatures.id,
                temperatures.city_id,
                temperatures.tmp_value,
                temperatures.tmp_timestamp
            FROM
                temperatures
            JOIN
                cities ON temperatures.city_id = cities.id
        """

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return query

    def get_temperatures_for_cities(self, latitude: float, longitude: float,
                         date_from: str, date_until: str, city_id: int) -> List[Temperature]:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        query = self.construct_query_temp_for_cities(
            latitude=latitude,
            longitude=longitude,
            date_from=date_from,
            date_until=date_until,
            city_id=city_id
        )

        temperatures = []
        rows = []
        with conn.cursor() as cursor:
            cursor.execute(query, ())
            rows = cursor.fetchall()
        conn.close()

        for row in rows:
            if row and row[0] and row[1] and row[2] and row[3]:
                temperatures.append(
                    Temperature(
                        id=row[0],
                        city_id=row[1],
                        value=float(row[2]),
                        timestamp=row[3].strftime("%Y-%m-%d")
                    )
                )

        return temperatures

    def get_temperatures_for_countries(self, latitude: float, longitude: float,
                         date_from: str, date_until: str, country_id: int) -> List[Temperature]:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        query = self.construct_query_temp_for_countries(
            latitude=latitude,
            longitude=longitude,
            date_from=date_from,
            date_until=date_until,
            country_id=country_id
        )

        temperatures = []
        rows = []
        with conn.cursor() as cursor:
            cursor.execute(query, ())
            rows = cursor.fetchall()
        conn.close()

        for row in rows:
            if row and row[0] and row[1] and row[2] and row[3]:
                temperatures.append(
                    Temperature(
                        id=row[0],
                        city_id=row[1],
                        value=float(row[2]),
                        timestamp=row[3].strftime("%Y-%m-%d")
                    )
                )

        return temperatures

    def update_temperature_in_db(self, id: int, city_id, value: float) -> StatusCode:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        update_data_tuple = (
            str(value),
            id
        )

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM temperatures WHERE id = %s", (id,))
                result = cursor.fetchone()

                # temperature doesn't exist in database
                if result is None:
                    return StatusCode.NOT_FOUND

                cursor.execute(UPDATE_TEMPERATURE_REQUEST, update_data_tuple)

        except pymysql.IntegrityError:
            conn.rollback()
            return StatusCode.CONFLICT

        finally:
            conn.commit()
            conn.close()

        return StatusCode.SUCCESS

    def delete_temperature_from_db(self, id: int) -> StatusCode:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM temperatures WHERE id = %s", (id,))
            result = cursor.fetchone()

            # temperature doesn't exist in database
            if result is None:
                return StatusCode.NOT_FOUND

            cursor.execute(DELETE_TEMPERATURE_REQUEST, (id,))

        conn.commit()
        conn.close()

        return StatusCode.SUCCESS