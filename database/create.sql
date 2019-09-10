CREATE DATABASE scraper;

\c scraper

CREATE TABLE temp (
	id SERIAL PRIMARY KEY,
	url VARCHAR (2100) NOT NULL
);

CREATE TABLE movie (
	id SERIAL PRIMARY KEY,
	url VARCHAR (2100) NOT NULL UNIQUE,
	title VARCHAR (50),
	release_date VARCHAR (50),
	summary VARCHAR (2100),
	reviews VARCHAR (2100),
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


\copy temp (url) FROM '/Users/Athya/documents/web-scraper/scraper/movieLinks.csv' WITH (FORMAT CSV, DELIMITER ',');

INSERT INTO movie (url) SELECT DISTINCT url FROM temp 