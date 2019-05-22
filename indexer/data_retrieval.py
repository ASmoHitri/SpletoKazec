import sqlite3



def get_query_results(query_string):
    query_words = query_string.split()

    connection = sqlite3.connect(db_file)
    query = "SELECT * FROM Posting WHERE word IN (?)"
    cursor = connection.cursor()

