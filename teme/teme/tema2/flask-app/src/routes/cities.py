import logging
from flask import request, jsonify
from src.database.database import DatabaseDriver
from src.utils import StatusCode

class CitiesRoutes():
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def check_args(self, **kwargs) -> bool:
        try:
            for arg_name, arg_value in kwargs.items():
                if arg_value is None:
                    continue
                if arg_name in ["nume"]:
                    str(arg_value)
                if arg_name in ["id", "country_id"]:
                    int(arg_value)
                elif arg_name in ["latitude", "longitude"]:
                    float(arg_value)
        except ValueError:
            return False
        
        return True
    
    def post_or_get_cities(self):
        if request.method == "GET":
            db_driver = DatabaseDriver(logger=self.logger)

            cities = db_driver.get_all_cities()

            results = []
            for city in cities:
                city_dict = city.return_dict()
                results.append(city_dict)
            
            return jsonify(results), StatusCode.SUCCESS.value
        elif request.method == "POST":
            json_data = request.get_json()

            if json_data is None:
                return jsonify({"error": "Invalid JSON data"}), StatusCode.BAD_REQUEST.value
            
            if "idTara" not in json_data:
                return jsonify({"error": "idTara was not provided"}), StatusCode.BAD_REQUEST.value
            elif "nume" not in json_data:
                return jsonify({"error": "nume was not provided"}), StatusCode.BAD_REQUEST.value
            elif "lon" not in json_data:
                return jsonify({"error": "lon was not provided"}), StatusCode.BAD_REQUEST.value
            elif "lat" not in json_data:
                return jsonify({"error": "lat was not provided"}), StatusCode.BAD_REQUEST.value
        
            country_id = json_data.get("idTara")
            name = json_data.get("nume")
            longitude = json_data.get("lon")
            latitude = json_data.get("lat")

            check_args = self.check_args(
                name=name,
                longitude=longitude,
                latitude=latitude,
                country_id=country_id
            )

            if not check_args:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
            
            db_driver = DatabaseDriver(logger=self.logger)
            result = db_driver.insert_new_city(
                country_id=country_id,
                name=name,
                latitude=latitude,
                longitude=longitude
            )

            if result[0] == StatusCode.CREATED:
                return jsonify({"id": result[1]}), StatusCode.CREATED.value
            elif result[0] == StatusCode.NOT_FOUND:
                return jsonify({"error": "Resource was not found!"}), StatusCode.NOT_FOUND.value
            elif result[0] == StatusCode.CONFLICT:
                return jsonify({"error": "Conflict during insertion"}), StatusCode.CONFLICT.value
            else:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
 
    def get_cities_for_country(self, country_id):
        if request.method == "GET":
            check_args = self.check_args(
                country_id=country_id
            )

            if not check_args:
                return jsonify([]), StatusCode.SUCCESS.value

            db_driver = DatabaseDriver(logger=self.logger)

            cities = db_driver.get_cities_for_country(country_id=int(country_id))

            results = []
            for city in cities:
                city_dict = city.return_dict()
                results.append(city_dict)
            
            return jsonify(results), StatusCode.SUCCESS.value

    def put_or_delete_city(self, id):
        if request.method == "PUT":
            json_data = request.get_json()

            if json_data is None:
                return jsonify({"error": "Invalid JSON data"}), StatusCode.BAD_REQUEST.value

            if "id" not in json_data:
               return jsonify({"error": "id was not provided"}), StatusCode.BAD_REQUEST.value
            if "idTara" not in json_data:
                return jsonify({"error": "idTara was not provided"}), StatusCode.BAD_REQUEST.value
            elif "nume" not in json_data:
                return jsonify({"error": "nume was not provided"}), StatusCode.BAD_REQUEST.value
            elif "lon" not in json_data:
                return jsonify({"error": "lon was not provided"}), StatusCode.BAD_REQUEST.value
            elif "lat" not in json_data:
                return jsonify({"error": "lat was not provided"}), StatusCode.BAD_REQUEST.value
        
            country_id = json_data.get("idTara")
            name = json_data.get("nume")
            longitude = json_data.get("lon")
            latitude = json_data.get("lat")

            check_args = self.check_args(
                name=name,
                longitude=longitude,
                latitude=latitude,
                country_id=country_id,
                id=id
            )

            if not check_args:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
            
            if json_data.get("id") != int(id):
                return jsonify({"error": "id doesn't match"}), StatusCode.BAD_REQUEST.value

            db_driver = DatabaseDriver(logger=self.logger)
            result = db_driver.update_city_in_db(
                id=int(id),
                country_id=country_id,
                name=name,
                latitude=latitude,
                longitude=longitude
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

            result = db_driver.delete_city_from_db(id=int(id))

            if result == StatusCode.SUCCESS:
                return jsonify({"message": "Success!"}), StatusCode.SUCCESS.value
            elif result == StatusCode.NOT_FOUND:
                return jsonify({"error": "Resource was not found!"}), StatusCode.NOT_FOUND.value
            else:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
