import sqlite3
import indexer.config as conf
from indexer.text_retrieval import process_text


def print_results(results, query_string):
    print("RESULTS FOR QUERY: ", query_string)
    print("Frequency | Document name                            | Snippet                                          ")
    print("---------- ------------------------------------------ --------------------------------------------------")
    for result in results:
        # TODO dokoncaj...
        print()



def get_query_results(query_string):
    query_tokens = [token for token, idx in process_text(query_string)]
    # print(query_tokens)
    connection = sqlite3.connect(conf.db_file)
    cursor = connection.cursor()
    query = "SELECT * FROM Posting WHERE word IN ({})"
    cursor.execute(query.format(','.join("?" * len(query_tokens))), tuple(query_tokens))
    results = cursor.fetchall()
    connection.close()

    # group results
    results_dict = {}
    for word, doc, freq, idxs in results:
        if doc in results_dict:
            results_dict[doc][0] += freq
            results_dict[doc][1].append((word, idxs))
        else:
            results_dict[doc] = [freq, [(word, idxs)], doc]

    # sort dictionary by frequency descending
    results = sorted(results_dict.values(), key=lambda x: x[0])
    if len(results) > 5:
        results = results[:5]
    print_results(results, query_string)


if __name__ == "__main__":
    get_query_results("sklenejo načina poročati")
