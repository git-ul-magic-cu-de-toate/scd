import logging
from flask import Flask
from src.routes.countries import CountriesRoutes
from src.routes.cities import CitiesRoutes
from src.routes.temperatures import TemperaturesRoutes


class WeatherAppServer():
    app: Flask

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.app = Flask(__name__)
        self.app.add_url_rule("/api/countries", view_func=self.post_or_get_countries, methods=["GET", "POST"])
        self.app.add_url_rule("/api/countries/<id>", view_func=self.put_or_delete_country, methods=["PUT", "DELETE"])
        self.app.add_url_rule("/api/cities", view_func=self.post_or_get_cities, methods=["GET", "POST"])
        self.app.add_url_rule("/api/cities/country/<country_id>", view_func=self.get_cities_for_country, methods=["GET"])
        self.app.add_url_rule("/api/cities/<id>", view_func=self.put_or_delete_city, methods=["PUT", "DELETE"])
        self.app.add_url_rule("/api/temperatures", view_func=self.post_or_get_temperatures, methods=["GET", "POST"])
        self.app.add_url_rule("/api/temperatures/cities/<city_id>", view_func=self.get_temperatures_for_city, methods=["GET"])
        self.app.add_url_rule("/api/temperatures/countries/<country_id>", view_func=self.get_temperatures_for_country, methods=["GET"])
        self.app.add_url_rule("/api/temperatures/<id>", view_func=self.put_or_delete_temperature, methods=["PUT", "DELETE"])

    def run(self):
        self.app.run(host="0.0.0.0", port=5000)

    def post_or_get_countries(self):
        countries_routes = CountriesRoutes(logger=self.app.logger)

        return countries_routes.post_or_get_countries()

    def put_or_delete_country(self, id):
        countries_routes = CountriesRoutes(logger=self.app.logger)

        return countries_routes.put_or_delete_country(id=id)
    
    def post_or_get_cities(self):
        cities_routes = CitiesRoutes(logger=self.app.logger)

        return cities_routes.post_or_get_cities()
    
    def get_cities_for_country(self, country_id):
        cities_routes = CitiesRoutes(logger=self.app.logger)

        return cities_routes.get_cities_for_country(country_id=country_id)

    def put_or_delete_city(self, id):
        cities_routes = CitiesRoutes(logger=self.app.logger)

        return cities_routes.put_or_delete_city(id=id)
    
    def post_or_get_temperatures(self):
        temperatures_routes = TemperaturesRoutes(logger=self.app.logger)

        return temperatures_routes.post_or_get_temperatures()

    def get_temperatures_for_city(self, city_id):
        temperatures_routes = TemperaturesRoutes(logger=self.app.logger)

        return temperatures_routes.get_temperatures_for_city(city_id=city_id)
    
    def get_temperatures_for_country(self, country_id):
        temperatures_routes = TemperaturesRoutes(logger=self.app.logger)

        return temperatures_routes.get_temperatures_for_country(country_id=country_id)

    def put_or_delete_temperature(self, id):
        temperatures_routes = TemperaturesRoutes(logger=self.app.logger)

        return temperatures_routes.put_or_delete_temperature(id=id)