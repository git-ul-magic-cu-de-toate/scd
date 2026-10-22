import os

MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'countries_user')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'countries_pass')
MYSQL_DB = os.environ.get('MYSQL_DATABASE', 'countries_db')
MYSQL_PORT = 3306

UPDATE_COUNTRY_REQUEST = '''
UPDATE countries
SET
    country_name = %s,
    latitude = %s,
    longitude = %s
WHERE
    id = %s;
'''

DELETE_COUNTRY_REQUEST = '''
DELETE FROM countries
WHERE id = %s;
'''

INSERT_CITY_REQUEST = '''
INSERT INTO cities 
(country_id, city_name, latitude, longitude) VALUES (%s, %s, %s, %s)
'''

UPDATE_CITY_REQUEST = '''
UPDATE cities
SET
    city_name = %s,
    latitude = %s,
    longitude = %s
WHERE
    id = %s;
'''

DELETE_CITY_REQUEST = '''
DELETE FROM cities
WHERE id = %s;
'''

INSERT_TEMPERATURE_REQUEST = '''
INSERT INTO temperatures 
(city_id, tmp_value) VALUES (%s, %s)
'''

UPDATE_TEMPERATURE_REQUEST = '''
UPDATE temperatures
SET
    tmp_value = %s
WHERE
    id = %s;
'''

DELETE_TEMPERATURE_REQUEST = '''
DELETE FROM temperatures
WHERE id = %s;
'''