import os
import sqlite3
import logging
from indexer.text_retrieval import prepare_tokens
import indexer.config as conf


posting_update_query = "UPDATE Posting SET frequency=frequency+1, indexes=indexes || ',' || ? WHERE word=? AND documentName=?"
posting_insert_query = "INSERT INTO Posting(word, documentName, frequency, indexes) VALUES (?, ?, ?, ?)"
index_insert_query = "INSERT OR IGNORE INTO IndexWord(word) VALUES (?)"


def insert_into_db(tokens, document_name, db_connection):
    cursor = db_connection.cursor()
    for word, index in tokens:
        try:
            cursor.execute(index_insert_query, (word,))
            db_connection.commit()
            # update Posting if word-document pair already in it, add new Posting row otherwise
            cursor.execute(posting_update_query, (index, word, document_name))
            if cursor.rowcount == 0:
                cursor.execute(posting_insert_query, (word, document_name, 1, index))
            db_connection.commit()

        except sqlite3.Error as error:
            logging.error("Could not insert index into DB. Error message: " + error.args[0])


def create_index(data_path):
    """
        Create inverted index for HTML files located in subfolders in 'data_path'
    """
    connection = sqlite3.connect(conf.db_file)
    for folder in os.listdir(data_path):
        full_path = os.path.join(data_path, folder)
        if os.path.isdir(full_path):
            for file in os.listdir(full_path):
                # process file
                print(os.path.join(full_path, file))
                tokens = prepare_tokens(os.path.join(full_path, file))
                insert_into_db(tokens, os.path.basename(file), connection)
    connection.close()


if __name__ == "__main__":
    create_index(conf.data_path)
