"""Transforms our csv data into the graph."""
import csv

from dataclasses import WeightedGraph


def string_to_list(set_str: str) -> list:
    """Given a string in the format of the csv, return the a list of the items.
    >>> hashtags = string_to_list("{'FutureIsProgressive', 'ABetterDeal'}")
    >>> hashtags == {"FutureIsProgressive", "ABetterDeal"}
    True
    """
    stripped = set_str[2:-2]
    clean_str = stripped.replace('\'', '').replace(' ', '')
    hashtags = clean_str.split(',')
    return hashtags


def load_weighted_hashtags_graph(hashtags_data_file: str) -> WeightedGraph:
    """Return a book review WEIGHTED graph corresponding to the given datasets.

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

    return hashtag_graph


def load_weighted_hashtags_networkx(hashtags_data_file: str) -> WeightedGraph:
    """Return a book review WEIGHTED graph corresponding to the given datasets.

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

    return hashtag_graph


def add_edges(hashtags_data_file: str, graph: WeightedGraph) -> None:
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
                        graph.add_edge(lst[i], lst[j], 1)


if __name__ == '__main__':
    graph = load_weighted_hashtags_graph('total_filtered_politician.csv')
    graph_vertices = graph.get_vertices()
    for vertex in graph_vertices:
        num = str(graph_vertices[vertex].count)
        bias = str(graph_vertices[vertex].partisanship)
        if int(num) > 400:
            print(vertex + " " + num + " Amount of bias " + bias)
    add_edges('total_filtered_politician.csv', graph)
    from visualization import visualize_graph
    visualize_graph(graph)
