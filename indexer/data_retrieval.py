import re
import os
import sqlite3
import logging
import indexer.config as conf
from indexer import text_retrieval
from indexer.text_retrieval import prepare_tokens


def get_snippet(index, num_of_words, document_path):
    text = text_retrieval.get_text(document_path)
    split_text = text.split()
    start_index = int(index - (num_of_words - 1) / 2)
    end_index = int(index + num_of_words / 2)
    # make sure indexes are not out of range
    if start_index < 0:
        start_index = 0
    if end_index >= len(split_text):
        end_index = len(split_text) - 1

    snippet_words = split_text[start_index:end_index+1]
    return " ".join(snippet_words), end_index


def print_results(results, query_string):
    print("RESULTS FOR QUERY: ", query_string)
    frequency_str_len = 11
    document_name_len = 43
    print("Frequency | Document name                            | Snippet                                                                            ")
    print("---------- ------------------------------------------ ------------------------------------------------------------------------------------")

    # print(results)
    for result in results:      # result: 0 - frequencies sum, 1 - indexes, 2 - document name
        document_name = result[2]
        match = re.match("([a-zA-Z.\-]*)\.[0-9]*\.html", document_name)
        if match:
            indexes = sorted(result[1])
            num_of_indexes = len(indexes)
            last_position = indexes[0] - 1
            snippet_string = ""
            num_of_snippets = 0
            for i in range(num_of_indexes):
                num_of_words = 7  # number of words per snippet
                if indexes[i] <= last_position:
                    continue
                if num_of_snippets == 5:
                    break
                # show max (num_of_words + 1) words in snippet (+1 if two consecutive tokens)
                if i < num_of_indexes - 1 and indexes[i + 1] == indexes[i] + 1:
                    num_of_words += 1
                snippet, last_position = get_snippet(indexes[i], num_of_words,
                                                     conf.data_path + match.group(1) + "/" + document_name)
                snippet_string += snippet + " ... "
                num_of_snippets += 1
            frequency_string = str(result[0])
            frequency_string += " " * (frequency_str_len - len(frequency_string))
            document_name += " " * (document_name_len - len(document_name))
            print(frequency_string, document_name, " " + snippet_string)
        else:
            logging.error(
                "Could not get document's folder name - bad document name {}".format(document_name))


def get_query_results(query_string):
    query_tokens = [token for token, idx in text_retrieval.prepare_tokens(query_string, html=False)]
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
        idxs = list(map(int, idxs.split(",")))
        if doc in results_dict:
            results_dict[doc][0] += freq
            results_dict[doc][1] += idxs
        else:
            results_dict[doc] = [freq, idxs, doc]

    # sort dictionary by frequency descending
    results = sorted(results_dict.values(), key=lambda x: x[0])
    print_results(results, query_string)


def get_query_results_sequential(query_string, data_path=conf.data_path):
    query_tokens = [token for token, idx in text_retrieval.prepare_tokens(query_string, html=False)]
    results_dict = {}
    for folder in os.listdir(data_path):
        full_path = os.path.join(data_path, folder)
        if os.path.isdir(full_path):
            for file in os.listdir(full_path):
                # process file
                print(os.path.join(full_path, file))
                tokens = prepare_tokens(os.path.join(full_path, file))
                freq = 0
                idxs = []
                for word in tokens:
                    if word[0] in query_tokens:
                        freq += 1
                        idxs.append(word[1])
                if freq != 0:
                    results_dict[file] = [freq, idxs, file]
    results = sorted(results_dict.values(), key=lambda x: x[0])
    print_results(results, query_string)


if __name__ == "__main__":
    get_query_results_sequential("sklenejo načina poročati")
    # get_query_results("sklenejo načina poročati")
