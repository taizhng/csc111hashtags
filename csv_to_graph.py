"""Transforms our csv data into the graph.
CSC111 2021 Hashtag Partisanship, converting our tweets csv file into a WeightedGraph.

This is a file to filter out all the American politician hashtags into a csv file
from hydrated tweet files.

It contains the functions to take in a csv_file with information on a politician's name,
political affiliation as well as tweets in the hashtag, and return a WeightedGraph using one's
choice of weighting for the hashtag nodes and their connections.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the professors and TAs
in CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this CSC111 project,
please consult with us.

This file is Copyright (c) 2021 Jiajin Wu, Tai Zhang, and Kenneth Miura.
"""
import csv
from dataclasses import WeightedGraph


def load_weighted_hashtags_graph(hashtags_data_file: str, min_count: int) -> WeightedGraph:
    """Return a WEIGHTED graph corresponding to the given datasets.

    Preconditions:
        - reviews_file is the path to a CSV file corresponding to the book review data
          format described on the assignment handout
        - book_names_file is the path to a CSV file corresponding to the book data
          format described on the assignment handout
    """
    hashtag_graph = WeightedGraph()

    with open(hashtags_data_file, encoding="utf-8") as csv_file:
        next(csv_file)
        for row in csv.reader(csv_file):
            hashtags = row[2]
            party = int(row[1])
            lst = string_to_list(hashtags)
            for hashtag in lst:
                hashtag_graph.add_vertex(hashtag, party)

    add_edges(hashtags_data_file, hashtag_graph)

    hashtag_graph.remove_min_count(min_count)

    return hashtag_graph


def string_to_list(set_str: str) -> list:
    """Given a string in the format of the csv containing the respective hashtags, return a list of
    strings where each string corresponds to a hashtag.

    >>> hashtags = string_to_list("{'FutureIsProgressive', 'ABetterDeal'}")
    >>> hashtags == {"FutureIsProgressive", "ABetterDeal"}
    True
    """
    stripped = set_str[2:-2]
    clean_str = stripped.replace('\'', '').replace(' ', '')
    hashtags = clean_str.split(',')
    return hashtags


def add_edges(hashtags_data_file: str, hashtag_graph: WeightedGraph) -> None:
    """Adds edges to the graph based on strict connections in the same tweet."""
    with open(hashtags_data_file, encoding="utf-8") as csv_file:
        next(csv_file)
        for row in csv.reader(csv_file):
            hashtags = row[2]
            # party = int(row[1])
            lst = string_to_list(hashtags)
            if len(lst) > 1:
                for i in range(0, len(lst) - 1):
                    for j in range(i + 1, len(lst)):
                        hashtag_graph.add_edge(lst[i], lst[j], 1)


if __name__ == '__main__':
    graph = load_weighted_hashtags_graph('total_filtered_politician.csv', 40)
    graph_vertices = graph.get_vertices()
    # counter = 0
    # for vertex in graph_vertices:
    #     num = str(graph_vertices[vertex].count)
    #     bias = str(graph_vertices[vertex].partisanship)
    #     if int(num) > 20:
    #         counter += 1
    #         print(vertex + " " + num + " Amount of bias " + bias)
    # print(counter)
    networkx_graph = graph.to_networkx()

    # graph.remove_min_count(20)
    # from visualization import visualize_graph
    # visualize_graph(graph)

    import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 1000,
    #     'disable': ['E1136'],
    #     'extra-imports': ['csv', 'networkx'],
    #     'allowed-io': ['load_weighted_hashtags_graph', 'add_edges'],
    #     'max-nested-blocks': 4
    # })
