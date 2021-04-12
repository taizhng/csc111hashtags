"""Main dataclasses used for the project."""
from __future__ import annotations
from typing import Any, Union


DEMOCRATIC = 0
REPUBLICAN = 1

class _WeightedVertex:
    """A vertex in our weighted partisan graph, structured similarly to A3's book reviews.

    Instance Attributes:
        - item: The data stored in this vertex, representing a twitter user or a hashtag.
        - kind: The type of this vertex: 'user' or 'hashtag'.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.
        - count_dem: the amount of times a hashtag has appeared in a Democratic party's tweet.
        - count_rep: the amount of times a hashtag has appeared in a Republican party's tweet.
        - partisanship: a weighting between 0 and 1 showing the bias of a tweet.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - count != 0

    """
    item: Any
    neighbours: dict[_WeightedVertex, Union[int, float]]
    count_dem: int
    count_rep: int
    partisanship: float

    def __init__(self, item: Any, count: int, count_dem: int, count_rep: int) -> None:
        """Initialize a new vertex with the given item.

        This vertex is initialized with no neighbours.

        Preconditions:

        """
        self.item = item
        self.neighbours = {}
        self.count = count
        self.count_dem = count_dem
        self.count_rep = count_rep
        self.partisanship = count_rep

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def similarity_score_INSERT_NAME(self, other: _WeightedVertex) -> float:
        """Return the similarity score between two hashtags.

        This similarity score is calculated by:

        """
        # self_neighbours = set(self.neighbours.keys())
        # other_neighbours = set(other.neighbours.keys())
        # if self_neighbours == set() or other_neighbours == set():
        #     return 0.0
        # else:
        #     return len(self_neighbours.intersection(other_neighbours)) \
        #            / len(self_neighbours.union(other_neighbours))

    def similarity_score_INSERT_NAME_2(self, other: _WeightedVertex) -> float:
        """Return the similarity score between two hashtags.

        As explained in the title, this similarity score is calculated by:
        """
        # self_neighbours = set(self.neighbours.keys())
        # other_neighbours = set(other.neighbours.keys())
        # if self_neighbours == set() or other_neighbours == set():
        #     return 0.0
        # else:
        #     both_adj = self_neighbours.intersection(other_neighbours)
        #     same_weight = len({rev for rev in both_adj if
        #                        self.neighbours[rev] == other.neighbours[rev]})
        #     one_adj = len(self_neighbours.union(other_neighbours))
        #     return same_weight / one_adj

    def update_weighting_absolute(self, party: int) -> None:
        """Updates the weighting a given hashtag vertex using the party affiliation using
        a basic absolute count of tweets appeared.

        Preconditions:
        party == 0 or 1
        """
        if party == DEMOCRATIC:
            self.count_dem += 1
        # Otherwise, the party is republican
        else:
            self.count_rep += 1
        self.count += 1
        self.partisanship = self.count_rep / self.count


class WeightedGraph:
    """A weighted graph used to represent a hashtag network that keeps track of weightings.

    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[Any, _WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, party: int) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            -
        """

        if item not in self._vertices:
            if party == DEMOCRATIC:
                self._vertices[item] = _WeightedVertex(item, 1, 1, 0)
            else:
                self._vertices[item] = _WeightedVertex(item, 1, 0, 1)
        else:
            self._vertices[item].update_weighting_absolute(party)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float] = 1) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            print(item1 + " " + item2 + "BRUH")
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_weight(self, item1: Any, item2: Any) -> Union[int, float]:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def average_weight(self, item: Any) -> float:
        """Return the average weight of the edges adjacent to the vertex corresponding to item.

        Raise ValueError if item does not corresponding to a vertex in the graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return sum(v.neighbours.values()) / len(v.neighbours)
        else:
            raise ValueError

    def get_vertices(self) -> dict:
        """Returns the _vertices"""
        return self._vertices
