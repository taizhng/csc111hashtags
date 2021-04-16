"""
CSC111 2021 Hashtag Partisanship, dataclasses for the WeightedGraph

This is a file to filter out all the American politician hashtags into a csv file
from hydrated tweet files

This file holds our _WeightedHashtag and WeightedGraph classes.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the professors and TAs
in CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this CSC111 project,
please consult with us.

This file is Copyright (c) 2021 Jiajin Wu, Tai Zhang, and Kenneth Miura.
"""
from __future__ import annotations
from typing import Any
import networkx as nx

# These global variables represent the absolute weighting of bias, where 0 corresponds
# with a Democratic oriented tweet/hashtag and 1 for Republican.
DEMOCRATIC = 0
REPUBLICAN = 1


class _WeightedHashtag:
    """A weighted vertex for our partisan graph. Includes various information about the
    hashtag's use, with the neighbours dependent on the style of weighting chosen.

    Instance Attributes:
        - item: The name of the hashtag stored as a str
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights. See: neighbours_indirect function.
        - count: The absolute number of times the hashtag has appeared in a tweet.
        - count_dem: the amount of times a hashtag has appeared in a Democratic member's tweet.
        - count_rep: the amount of times a hashtag has appeared in a Republican member's tweet.
        - partisanship: a weighting between 0 and 1 showing the bias of a tweet. See weigh_bias

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - count_dem >= 0
        - count_rep >= 0
        - 0 <= partisanship <= 1

    """
    item: Any
    neighbours: dict[_WeightedHashtag, (float, float)]
    count: int
    count_dem: int
    count_rep: int
    partisanship: float

    def __init__(self, item: Any, total_count: int, count_dem: int, count_rep: int) -> None:
        """Initialize the hashtag using the item given, and setting its count, count_dem and
        count rep values.

        The vertex is initialized with no neighbours.

        Preconditions:
            - count >= 0
            - count_dem >= 0
            - count_rep >= 0

        """
        self.item = item
        self.neighbours = {}
        self.count = total_count
        self.count_dem = count_dem
        self.count_rep = count_rep
        self.partisanship = count_rep

    def degree(self) -> int:
        """Return the degree of this hashtag."""
        return len(self.neighbours)

    def update(self, party: int) -> None:
        """Updates the weighting a given hashtag vertex using the party affiliation and
        a basic absolute count of tweets appeared.

        Preconditions:
            - party == 0 or 1
        >>> g = WeightedGraph()
        >>> g.add_vertex("MAGA", 1)
        >>> g.get_weight_hashtag("MAGA") == 1.0
        True
        >>> g.add_vertex("MAGA", 0)
        >>> g.get_weight_hashtag("MAGA") == 0.5
        True
        """
        # If party value is Democratic, add one to count_dem.
        if party == DEMOCRATIC:
            self.count_dem += 1
        # Otherwise, the party is Republican
        else:
            self.count_rep += 1
        # Update the entire count
        self.count += 1
        self.partisanship = self.count_rep / self.count
        self.update_weighting_absolute()

    def update_weighting_absolute(self) -> None:
        """Updates the weighting of a vertex
        Recalculate the partisanship using the formula:
        # self.partisanship = (self.count_rep * REPUBLICAN + self.count_dem * DEMOCRATIC)/self.count
        # Since DEMOCRATIC == 0, we only count self.count_rep.
        """

        self.partisanship = self.count_rep / self.count


class WeightedGraph:
    """A weighted graph used to represent the connections between hashtags.
    Includes functions to update the graph, as well as retrieve information. A few functions
    modified from CSC111 Assignment 3.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of _WeightedHashtag contained in the graph.
    #         Maps item to _WeightedHashtag object.
    _vertices: dict[Any, _WeightedHashtag]

    def __init__(self) -> None:
        """Initialize an empty graph (no hashtag vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, party: int) -> None:
        """Add a vertex with the given item to this graph with the corresponding party affiliation.

        The new vertex is not adjacent to any other vertices.
        If the item is already in the graph, call the update_weighting_(CHOICE) function.

        Preconditions:
            - party == 0 or 1
        """

        if item not in self._vertices:
            # Create a new hashtag with an initial weighting of 0 for a democratic biased node.
            if party == DEMOCRATIC:
                self._vertices[item] = _WeightedHashtag(item, 1, 1, 0)
            # Create a new hashtag with an initial weighting of 1 for a Republican biased node.
            else:
                self._vertices[item] = _WeightedHashtag(item, 1, 0, 1)
        # If the node is already in the graph, update using the update_weighting_(CHOICE).
        else:

            self._vertices[item].update(party)

    def add_edge(self, item1: Any, item2: Any, weight_format: str) -> None:
        """Add an edge between the two hashtags with the given items in this graph,
        with the given weight. Modified from CSC111-A3

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
            - weight_format == 'absolute' or 'highest'
        """
        if item1 in self._vertices and item2 in self._vertices:

            # Add the new edge
            if weight_format == 'abs':
                self.update_edge_weight_absolute(item1, item2)
            else:
                self.update_edge_weight_highest(item1, item2)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def update_edge_weight_absolute(self, item1: Any, item2: Any) -> None:
        """Updates the edge weight based on the occurences of both hashtags.
        If #DACA occurs 10 times, #DREAMers occurs 8 times, and they occur together 6 times, the
        edge weighting would be 6/9.
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]

        new_denom = (v1.count + v2.count) / 2
        if v2 in v1.neighbours:
            og_count = v1.neighbours[v2][0]

            v1.neighbours[v2] = (og_count + 1, og_count / new_denom)
            v2.neighbours[v1] = (og_count + 1, og_count / new_denom)
        else:

            v1.neighbours[v2] = (1, 1 / new_denom)
            v2.neighbours[v1] = (1, 1 / new_denom)

    def update_edge_weight_highest(self, item1: Any, item2: Any) -> None:
        """Updates the edge weight based on the occurences of the least common hashtag.
        E.G. If #Trump has 100 occurences and #ImpeachTrump has 30 occurences, with 25 occurred
        with #Trump, the edge weighting would be 25/30.
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]

        if v1.count > v2.count:
            new_denom = v2.count
        else:
            new_denom = v1.count

        if v2 in v1.neighbours:
            og_count = v1.neighbours[v2][0]

            v1.neighbours[v2] = (og_count + 1, og_count / new_denom)
            v2.neighbours[v1] = (og_count + 1, og_count / new_denom)
        else:
            v1.neighbours[v2] = (1, 1 / new_denom)
            v2.neighbours[v1] = (1, 1 / new_denom)

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.
        Return False if item1/item2 are not in the graph. Modified from CSC111-A3
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_weight_edge(self, item1: Any, item2: Any) -> float:
        """Return the weight of the edge between the given items.

        Return -1 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, -1)[1]

    def get_weight_hashtag(self, item: Any) -> float:
        """Returns the weight of the partisanship of the hashtag.

        Returns -1.0 if item is not in the graph.

        Preconditions:
            - item in self._vertices"""
        return self._vertices[item].partisanship

    def get_vertices(self) -> dict:
        """Returns the _vertices of the graph."""
        return self._vertices

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Converts the weighted graph to the networkx graph, to be called after the
        computations have been completed. Creates a networkx graph including the partisanship
        bias, the weighting of the hashtag node (absolute number of times it has appeared),
        as well as all the weighted edges connecting the hashtag nodes."""
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, bias=v.partisanship, count=v.count)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, bias=u.partisanship, count=u.count)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item, weight=u.neighbours[v][1])

            if graph_nx.number_of_nodes() >= max_vertices:
                break
        return graph_nx

    def remove_min_count(self, min_count: int) -> None:
        """Removes nodes that have a count less than min_count.
        """
        new_graph = self._vertices.copy()
        for hashtag in self._vertices:
            if self._vertices[hashtag].count <= min_count:
                # REMOVING NEIGHBOURS TOO.
                for neighbour in new_graph[hashtag].neighbours:
                    if hashtag != neighbour.item:
                        neighbour.neighbours.pop(new_graph[hashtag])
                new_graph.pop(hashtag)
        self._vertices = new_graph
