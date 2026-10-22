import logging
import datetime
from flask import request, jsonify
from src.database.database import DatabaseDriver
from src.utils import StatusCode

class TemperaturesRoutes():
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def check_args(self, **kwargs) -> bool:
        try:
            for arg_name, arg_value in kwargs.items():
                if arg_value is None:
                    continue
                if arg_name in ["city_id", "country_id", "id"]:
                    int(arg_value)
                elif arg_name in ["latitude", "longitude", "value"]:
                    float(arg_value)
                elif arg_name in ["date_from", "date_until"]:
                    datetime.datetime.strptime(arg_value, "%Y-%m-%d")
        except ValueError:
            return False
        
        return True

    def post_or_get_temperatures(self):
        if request.method == "POST":
            json_data = request.get_json()

            if json_data is None:
                return jsonify({"error": "Invalid JSON data"}), StatusCode.BAD_REQUEST.value
            
            if "idOras" not in json_data:
                return jsonify({"error": "idOras was not provided"}), StatusCode.BAD_REQUEST.value
            elif "valoare" not in json_data:
                return jsonify({"error": "valoare was not provided"}), StatusCode.BAD_REQUEST.value
        
            city_id = json_data.get("idOras")
            value = json_data.get("valoare")

            check_args = self.check_args(
                city_id=city_id,
                value=value
            )

            if not check_args:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value

            db_driver = DatabaseDriver(logger=self.logger)
            result = db_driver.insert_new_temperature(
                city_id=city_id,
                value=value
            )

            if result[0] == StatusCode.CREATED:
                return jsonify({"id": result[1]}), StatusCode.CREATED.value
            elif result[0] == StatusCode.NOT_FOUND:
                return jsonify({"error": "Resource was not found!"}), StatusCode.NOT_FOUND.value
            elif result[0] == StatusCode.CONFLICT:
                return jsonify({"error": "Conflict during insertion"}), StatusCode.CONFLICT.value
            else:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
        elif request.method == "GET":
            latitude = request.args.get("lat")
            longitude = request.args.get("lon")
            date_from = request.args.get("from")
            date_until = request.args.get("until")

            check_args = self.check_args(
                latitude=latitude,
                longitude=longitude,
                date_from=date_from,
                date_until=date_until
            )

            if not check_args:
                return jsonify([]), StatusCode.SUCCESS.value

            db_driver = DatabaseDriver(logger=self.logger)

            temperatures_cities = db_driver.get_temperatures_for_cities(
                latitude=latitude,
                longitude=longitude,
                date_from=date_from,
                date_until=date_until,
                city_id=None
            )

            results = []
            for temperature in temperatures_cities:
                temperature_dict = temperature.return_dict()
                results.append(temperature_dict)
            
            if not latitude and not longitude:
                return jsonify(results), StatusCode.SUCCESS.value
            
            temperatures_countries = db_driver.get_temperatures_for_countries(
                latitude=latitude,
                longitude=longitude,
                date_from=date_from,
                date_until=date_until,
                country_id=None
            )

            for temperature in temperatures_countries:
                temperature_dict = temperature.return_dict()
                results.append(temperature_dict)

            return jsonify(results), StatusCode.SUCCESS.value

    def get_temperatures_for_city(self, city_id):
        if request.method == "GET":
            date_from = request.args.get("from")
            date_until = request.args.get("until")

            check_args = self.check_args(
                date_from=date_from,
                date_until=date_until,
                city_id=city_id
            )

            if not check_args:
                return jsonify([]), StatusCode.SUCCESS.value

            db_driver = DatabaseDriver(logger=self.logger)

            temperatures_cities = db_driver.get_temperatures_for_cities(
                latitude=None,
                longitude=None,
                date_from=date_from,
                date_until=date_until,
                city_id=city_id
            )

            results = []
            for temperature in temperatures_cities:
                temperature_dict = temperature.return_dict()
                results.append(temperature_dict)
            
            return jsonify(results), StatusCode.SUCCESS.value

    def get_temperatures_for_country(self, country_id):
        if request.method == "GET":
            date_from = request.args.get("from")
            date_until = request.args.get("until")

            check_args = self.check_args(
                date_from=date_from,
                date_until=date_until,
                country_id=country_id
            )

            if not check_args:
                return jsonify([]), StatusCode.SUCCESS.value

            db_driver = DatabaseDriver(logger=self.logger)

            temperatures_cities = db_driver.get_temperatures_for_countries(
                latitude=None,
                longitude=None,
                date_from=date_from,
                date_until=date_until,
                country_id=country_id
            )

            results = []
            for temperature in temperatures_cities:
                temperature_dict = temperature.return_dict()
                results.append(temperature_dict)
            
            return jsonify(results), StatusCode.SUCCESS.value

    def put_or_delete_temperature(self, id):
        if request.method == "PUT":
            json_data = request.get_json()

            if json_data is None:
                return jsonify({"error": "Invalid JSON data"}), StatusCode.BAD_REQUEST.value

            if "id" not in json_data:
               return jsonify({"error": "id was not provided"}), StatusCode.BAD_REQUEST.value
            if "idOras" not in json_data:
                return jsonify({"error": "idOras was not provided"}), StatusCode.BAD_REQUEST.value
            elif "valoare" not in json_data:
                return jsonify({"error": "valoare was not provided"}), StatusCode.BAD_REQUEST.value
        
            city_id = json_data.get("idOras")
            args_id = json_data.get("id")
            value = json_data.get("valoare")

            check_args = self.check_args(
                value=value,
                city_id=city_id,
                id=id
            )

            if not check_args:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
            
            if json_data.get("id") != int(id):
                return jsonify({"error": "id doesn't match"}), StatusCode.BAD_REQUEST.value

            db_driver = DatabaseDriver(logger=self.logger)
            result = db_driver.update_temperature_in_db(
                id=args_id,
                city_id=city_id,
                value=value
            )

            if result == StatusCode.SUCCESS:
                return jsonify({"message":"Success!"}), StatusCode.SUCCESS.value
            elif result == StatusCode.NOT_FOUND:
                return jsonify({"error": "Resource was not found!"}), StatusCode.NOT_FOUND.value
            elif result == StatusCode.CONFLICT:
                return jsonify({"error": "Conflict during insertion"}), StatusCode.CONFLICT.value
            else:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
        elif request.method == "DELETE":
            if not id:
                return jsonify({"error": "id was not provided"}), StatusCode.BAD_REQUEST.value

            check_args = self.check_args(
                id=id
            )

            if not check_args:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
            
            db_driver = DatabaseDriver(logger=self.logger)

            result = db_driver.delete_temperature_from_db(id=int(id))

            if result == StatusCode.SUCCESS:
                return jsonify({"message": "Success!"}), StatusCode.SUCCESS.value
            elif result == StatusCode.NOT_FOUND:
                return jsonify({"error": "Resource was not found!"}), StatusCode.NOT_FOUND.value
            else:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
