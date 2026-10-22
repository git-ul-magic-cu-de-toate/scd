from dataclasses import dataclass
from enum import Enum

class StatusCode(Enum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409

@dataclass
class Country:
    id: int
    name: str
    latitude: float
    longitude: float

    def return_dict(self):
        country_dict = {
            "id": self.id,
            "nume": self.name,
            "lat": self.latitude,
            "lon": self.longitude
        }

        return country_dict


@dataclass
class City:
    id: int
    country_id: int
    name: str
    latitude: float
    longitude: float

    def return_dict(self):
        city_dict = {
            "id": self.id,
            "idTara": self.country_id,
            "nume": self.name,
            "lat": self.latitude,
            "lon": self.longitude
        }

        return city_dict

@dataclass
class Temperature:
    id: int
    city_id: int
    value: float
    timestamp: str

    def return_dict(self):
        temp_dict = {
            "id": self.id,
            "valoare": self.value,
            "timestamp":  self.timestamp
        }

        return temp_dict

