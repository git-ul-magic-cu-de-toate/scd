use countries_db;

CREATE TABLE countries (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  country_name VARCHAR(255) NOT NULL UNIQUE,
  latitude VARCHAR(30) NOT NULL,
  longitude VARCHAR(30) NOT NULL
);

CREATE TABLE cities (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  country_id INT NOT NULL,
  city_name VARCHAR(255) NOT NULL,
  latitude VARCHAR(30) NOT NULL,
  longitude VARCHAR(30) NOT NULL,
  FOREIGN KEY (country_id) REFERENCES countries(id),
  UNIQUE(country_id, city_name)
);

CREATE TABLE temperatures (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  tmp_value VARCHAR(30),
  tmp_timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),
  city_id INT NOT NULL,
  FOREIGN KEY (city_id) REFERENCES cities(id),
  UNIQUE(city_id, tmp_timestamp)
);