import logging
from flask import request, jsonify
from src.database.database import DatabaseDriver
from src.utils import StatusCode

class CountriesRoutes():
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
                if arg_name in ["id"]:
                    int(arg_value)
                elif arg_name in ["latitude", "longitude"]:
                    float(arg_value)
        except ValueError:
            return False
        
        return True

    def post_or_get_countries(self):
        if request.method == "GET":
            db_driver = DatabaseDriver(logger=self.logger)
            countries = db_driver.get_all_countries()

            results = []
            for country in countries:
                country_dict = country.return_dict()
                results.append(country_dict)

            return jsonify(results), StatusCode.SUCCESS.value
        elif request.method == "POST":
            json_data = request.get_json()

            if json_data is None:
                return jsonify({"error": "Invalid JSON data"}), StatusCode.BAD_REQUEST.value
            
            if "nume" not in json_data:
                return jsonify({"error": "nume was not provided"}), StatusCode.BAD_REQUEST.value
            elif "lon" not in json_data:
                return jsonify({"error": "lon was not provided"}), StatusCode.BAD_REQUEST.value
            elif "lat" not in json_data:
                return jsonify({"error": "lat was not provided"}), StatusCode.BAD_REQUEST.value
                          
            name = json_data.get("nume")
            longitude = json_data.get("lon")
            latitude = json_data.get("lat")

            check_args = self.check_args(
                name=name,
                longitude=longitude,
                latitude=latitude
            )

            if not check_args:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
                
            db_driver = DatabaseDriver(logger=self.logger)
            id = db_driver.insert_new_country(
                name=name,
                latitude=latitude,
                longitude=longitude
            )
        
            if id == -1:
                return jsonify({"error": "Conflict during insertion"}), StatusCode.CONFLICT.value
            
            id_dict = {"id": id}
            
            return jsonify(id_dict), StatusCode.CREATED.value
    
    def put_or_delete_country(self, id: int):
        if request.method == "PUT":
            json_data = request.get_json()
            
            if json_data is None:
                return jsonify({"error": "Invalid JSON data"}), StatusCode.BAD_REQUEST.value

            if "id" not in json_data:
                return jsonify({"error": "id was not provided"}), StatusCode.BAD_REQUEST.value                          
            elif "nume" not in json_data:
                return jsonify({"error": "nume was not provided"}), StatusCode.BAD_REQUEST.value
            elif "lon" not in json_data:
                return jsonify({"error": "lon was not provided"}), StatusCode.BAD_REQUEST.value
            elif "lat" not in json_data:
                return jsonify({"error": "lat was not provided"}), StatusCode.BAD_REQUEST.value
            
            req_id = json_data.get("id")
            name = json_data.get("nume")
            longitude = json_data.get("lon")
            latitude = json_data.get("lat")

            check_args = self.check_args(
                name=name,
                longitude=longitude,
                latitude=latitude,
                id=req_id
            )

            if not check_args:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value

            if json_data.get("id") != int(id):
                return jsonify({"error": "id doesn't match"}), StatusCode.BAD_REQUEST.value     
            
            db_driver = DatabaseDriver(logger=self.logger)

            result = db_driver.update_country_in_db(
                id=req_id,
                name=name,
                longitude=longitude,
                latitude=latitude
            )

            if result == StatusCode.SUCCESS:
                return jsonify({"message": "Success!"}), StatusCode.SUCCESS.value
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

            result = db_driver.delete_country_from_db(id=int(id))

            if result == StatusCode.SUCCESS:
                return jsonify({"message": "Success!"}), StatusCode.SUCCESS.value
            elif result == StatusCode.NOT_FOUND:
                return jsonify({"error": "Resource was not found!"}), StatusCode.NOT_FOUND.value
            else:
                return jsonify({"error": "Bad Request"}), StatusCode.BAD_REQUEST.value
