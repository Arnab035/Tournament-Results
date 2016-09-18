-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--Players table

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;


DROP TABLE if exists players;

CREATE TABLE players(
	player_id serial PRIMARY KEY,
    player_name text NOT NULL
 );

--matches table

DROP TABLE if exists matches;

CREATE TABLE matches(
	match_id serial PRIMARY KEY ,
	player_winner integer REFERENCES players(player_id ) ON DELETE CASCADE,
	player_loser integer REFERENCES players(player_id) ON DELETE CASCADE,
	UNIQUE (player_winner, player_loser),                       --to avoid matches between the same set of players
	CHECK(player_winner <> player_loser)
);

CREATE VIEW player_standings AS
	SELECT c.id AS player_id, p.player_name, c.x AS wins, (SELECT count(*)/2 FROM matches) AS matches
	FROM players p join (SELECT p.player_id as id, count(m.player_winner) AS x
		FROM players p LEFT JOIN matches m
		ON p.player_id = m.player_winner
		GROUP BY p.player_id
		ORDER BY x DESC) c
	ON p.player_id = c.id
	ORDER BY x DESC;








