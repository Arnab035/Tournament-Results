#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print("error trying to connect")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()

    # deletes all the matches from the table
    c.execute("delete from matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    # deletes all the players from the table
    c.execute("delete from players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()

    # this query returns the number of players registered
    query = "select count(*) from players"
    c.execute(query)
    value = c.fetchone()

    # value is  returned as a tuple but we want only the
    # value of the number of players
    # hence we select only the first element of the tuple
    db.close()
    return value[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()

    # registering a player for the tournament
    c.execute("insert into players(player_name) values (%s)", (name, ))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    # player_standings is a view which has sorted
    # the list of players as per the number of matches they won
    # in descending order
    query = "select * from player_standings"
    c.execute(query)
    rows = c.fetchall()
    db.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    # insertion of winner and the loser for a particular match
    c.execute("insert into matches(player_winner,player_loser) values (%s,%s)",
              (winner, loser, ))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # playerStandings fetches the current player standings based on a view
    # player_standings
    standings = playerStandings()

    # count contains the number of players
    count = len(standings)
    pairs = []
    if (count % 2 == 0):
        i = 0
    # pairs is a list of tuples that will contain the swiss-system pairs
        while (i < count):
            # the swiss-system pairs are based on selecting adjacent
            # players from the list of player standings
            row = standings[i]
            next_row = standings[i+1]
            pairs.append((row[0], row[1], next_row[0], next_row[1]))

        # iterate over two elements
            i = i + 2
    return pairs
