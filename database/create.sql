CREATE DATABASE scraper;

\c scraper

CREATE TABLE movie (
	id SERIAL PRIMARY KEY,
	url VARCHAR (2100) NOT NULL,
	movie_title VARCHAR (50),
	release_date VARCHAR (50),
	summary VARCHAR (2100),
	reviews VARCHAR (2100),
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


\copy movie (url) FROM '/Users/Athya/documents/web-scraper/scraper/movieLinks.csv' WITH (FORMAT CSV, DELIMITER ',');