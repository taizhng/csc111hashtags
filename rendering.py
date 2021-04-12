import random
from typing import List, Tuple

import networkx as nx
import matplotlib
from matplotlib.axes import Axes

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk

partisanship_range = [0, 1]


def generate_dummy_graph(num_nodes: int) -> nx.Graph:
    g = nx.Graph()

    for i in range(num_nodes):
        partisanship = random.uniform(partisanship_range[0], partisanship_range[1])

        node_name = f'Node {i}'
        g.add_node(node_name, partisanship=partisanship)
    for i in range(num_nodes):
        node_name = f'Node {i}'
        if random.random() > 0.5:
            connected_node_name = f'Node {random.randrange(0, num_nodes)}'
            g.add_edge(node_name, connected_node_name)

    return g


def render_neighbours(graph: nx.Graph, graph_plot: Axes, selected_node_name: str) -> None:
    nodes = [selected_node_name]
    edges = []
    for neighbour in graph.neighbors(selected_node_name):
        print(f'{selected_node_name} is neighbour to {neighbour}')
        nodes.append(neighbour)
        edges.append((selected_node_name, neighbour))

    blue_to_red = colors.LinearSegmentedColormap.from_list("BlueToRed", ["b", "r"])
    node_colours = [graph.nodes[node_name]['partisanship'] for node_name in nodes]
    # TODO: iron out bug where the colour of node changes for this vs what it originally was
    nx.draw(g, cmap=blue_to_red, node_color=node_colours, nodelist=nodes, edgelist=edges,
            with_labels=True, ax=graph_plot)


def render_graph(graph: nx.Graph, num_nodes: int) -> Tuple[List[str], List[Tuple[str, str]]]:
    '''
     Note: The first element of the tuple contains the nodes, and the second element of the tuple
    is the list of edges

    '''
    # choose a random vertex
    # maybe just use this: https://networkx.org/documentation/stable//reference/classes/generated/networkx.Graph.subgraph.html#networkx.Graph.subgraph
    nodes = []
    edges = []
    unvisited_nodes = set(graph.nodes)
    while num_nodes > 0:
        start_node = random.choice(tuple(unvisited_nodes))
        # either continue randomly selecting choices till it hasn't been visited, or remove nodes that are in the list
        # I'm pretty sure doing removal in the set and then choosing from the set as a tuple is faster? in terms of Big O
        nodes_clump, edges_clump = _get_nodes_and_edges(graph, start_node, num_nodes, set())
        num_nodes -= len(nodes_clump)
        nodes.extend(nodes_clump)
        edges.extend(edges_clump)
        for node in nodes_clump:
            unvisited_nodes.remove(node)

    return nodes, edges
    # NOTE: unfinished, and doesn't work


def _get_nodes_and_edges(graph: nx.Graph, current_node_name: str, num_nodes: int,
                         visited: set[str]) -> \
        Tuple[List[str], List[Tuple[str, str]]]:
    """ return tuple of list of num_nodes nodes, and a list of the edges between them.

    Decides which nodes to include by choosing random vertices, and including all connected vertices
    till num_nodes hit

    Note: The first element of the tuple contains the nodes, and the second element of the tuple
    is the list of edges


    Preconditions:
        - graph nodes have unique names

    """
    if num_nodes == 0:
        print(f'number of nodes left{num_nodes}')
        return ([], [])
    else:
        nodes = [current_node_name]
        edges = []
        visited.add(current_node_name)
        for neighbour in graph.neighbors(current_node_name):
            if neighbour not in visited:
                edges.append((current_node_name, neighbour))
                neighbour_nodes, neighbours_edges = _get_nodes_and_edges(graph, neighbour,
                                                                         num_nodes - 1, visited)
                nodes.extend(neighbour_nodes)
                edges.extend(neighbours_edges)
        return (nodes, edges)

    # This should be really similar to a graph traversal algorithm?
    # Should make list "nodelist", which we pass to the draw method
    # also make list "edgelist" that we pass to draw method


def render_tkinter_gui(graph: nx.Graph, graph_figure: plt.Figure, nodes_list: List[str]):
    """ Renders the graph

    """
    window = tk.Tk()

    frame_graph = tk.Frame(master=window, width=100)
    frame_graph.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
    canvas = FigureCanvasTkAgg(graph_figure, master=frame_graph)
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, frame_graph, pack_toolbar=False)
    toolbar.update()

    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frame_user_interaction = tk.Frame(master=window, width=200, height=100)
    frame_user_interaction.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    selected_node_name = tk.StringVar()
    # could maybe add autocomplete feature?
    node_selector = ttk.Combobox(master=frame_user_interaction,
                                 textvariable=selected_node_name)
    partisanship_label = ttk.Label(master=frame_user_interaction)
    partisanship_label.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def on_combobox_selected(event):
        # I hate this method and all it represents
        # I think if I make all the tkinter stuff an object this becomes less bad?
        print("combobox selected")
        print(f'The selected combobox is: {selected_node_name.get()}')
        selected_node_partisanship = graph.nodes[selected_node_name.get()]['partisanship']
        partisanship_label['text'] = f'Partisanship score is: \n {selected_node_partisanship}'

        graph_plot = graph_figure.get_axes()[0]
        graph_plot.clear()
        render_neighbours(graph, graph_plot, selected_node_name.get())
        canvas.draw()

    node_selector['values'] = nodes_list
    node_selector.state(['readonly'])
    node_selector.bind("<<ComboboxSelected>>", on_combobox_selected)
    node_selector.pack()
    # NOTE: when value changes, call selection_clear method

    window.mainloop()


if __name__ == '__main__':
    # https://stackoverflow.com/questions/20133479/how-to-draw-directed-graphs-using-networkx-in-python
    g = generate_dummy_graph(50)
    num_nodes = 7
    n_nodes, n_edges = render_graph(g, num_nodes)
    print(f'correct number of nodes: {len(n_nodes) == num_nodes}')
    print(n_nodes)
    node_colours = [g.nodes[node_name]['partisanship'] for node_name in n_nodes]

    # Color map stuff: https://stackoverflow.com/questions/25748183/python-making-color-bar-that-runs-from-red-to-blue
    blue_to_red = colors.LinearSegmentedColormap.from_list("BlueToRed", ["b", "r"])
    graph_figure = plt.Figure()
    a = graph_figure.add_subplot(111)
    spring_pos = nx.spring_layout(g)
    # Try just drawing nodes -> draw edges -> draw layers
    labels = {}
    for node in n_nodes:
        labels[node] = node
    nx.draw(g, pos=spring_pos, cmap=blue_to_red, node_color=node_colours, with_labels=True, ax=a,
            nodelist=n_nodes, labels=labels, edgelist=n_edges)

    render_tkinter_gui(g, graph_figure, list(g.nodes))

    # TODO:
    # figure out how to intelligently limit number of vertices (Basically done)
    #
    # https://stackoverflow.com/questions/55553845/display-networkx-graph-inside-the-tkinter-window
    # make it so it doesn't recalculate color when u open a new graph lol

    # NOTE: Jeremy, this is your stuff
    # Why does the application glitch when the mouse is in the boundaries?
    #   - glitching only happens in pan mode, when the graph is in tkinter.
    #   - is this just networkX? Or anything through matplotlib
    #   - Does this happen when you render the whole graph?

    # Tkinter: https://realpython.com/python-gui-tkinter/
    # TODO: maybe refactor so all the tkinter stuff is in a class? May be easier to interact with then
