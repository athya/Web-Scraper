CREATE DATABASE scraper;

\c scraper

CREATE TABLE temp (
	id SERIAL PRIMARY KEY,
	url VARCHAR (2100) NOT NULL
);

CREATE TABLE unscraped_url (
	id SERIAL PRIMARY KEY,
	url VARCHAR (2100) NOT NULL UNIQUE
);

CREATE TABLE movie (
	id SERIAL PRIMARY KEY,
	url VARCHAR (2100) NOT NULL UNIQUE,
	title VARCHAR (50),
	director VARCHAR (50),
	distributor VARCHAR (50),
	release_date VARCHAR (50),
	genres VARCHAR (100),
	rating VARCHAR (10),
	metascore VARCHAR (10),
	summary VARCHAR (2100),
	actors VARCHAR (200),
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
 -- test on delete cascade!
CREATE TABLE review (
	id SERIAL PRIMARY KEY,
	movie_id INT REFERENCES movie(id) ON DELETE CASCADE,
	url VARCHAR (2100) NOT NULL,
	content VARCHAR (5000)
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)


\copy temp (url) FROM '/Users/Athya/documents/web-scraper/scraper/movieLinks.csv' WITH (FORMAT CSV, DELIMITER ',');

INSERT INTO unscraped_url (url) SELECT DISTINCT url FROM temp 