"""CSC111 Winter 2021 Final assignment Rendering

Description
===============================
This python module provides an implementation for viewing the graph of hashtags, as well as an
interface for interacting with it.
Copyright and Usage Information
===============================
This file is provided solely for the final assignment of CSC110 at the University of Toronto
St. George campus. All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.
This file is Copyright (c) 2021 Kenneth Miura
"""
import random
from typing import List, Tuple
import tkinter as tk
from tkinter import ttk

import networkx as nx
import matplotlib

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from plotly.graph_objs import Scatter, Figure

matplotlib.use("TkAgg")

PARTISANSHIP_RANGE = [0, 1]
DEFAULT_NODES_TO_RENDER = 20


def generate_dummy_graph(num_nodes: int) -> nx.Graph:
    """
    Creates a weighted graph, in order to test GUI

    """
    graph = nx.Graph()
    threshold_for_edge = 0.5

    for i in range(num_nodes):
        partisanship = random.uniform(PARTISANSHIP_RANGE[0], PARTISANSHIP_RANGE[1])

        node_name = f'Node {i}'
        graph.add_node(node_name, bias=partisanship)
    for i in range(num_nodes):
        node_name = f'Node {i}'
        if random.random() > threshold_for_edge:
            connected_node_name = f'Node {random.randrange(0, num_nodes)}'
            graph.add_edge(node_name, connected_node_name)

    return graph


def draw_all_nodes_no_labels(graph: nx.Graph, graph_plot: Axes):
    ''' Draw all nodes and edges in the graph, but no labels

    '''
    nodes = list(graph.nodes)
    edge_width = 0.1
    edge_transparency = 0
    node_size = 50

    node_colours = [get_colour(graph.nodes[node_name]['bias']) for node_name in nodes]
    spring_pos = nx.spring_layout(nodes)
    if graph_plot is None:
        nx.draw_networkx_nodes(graph, spring_pos, node_color=node_colours, node_size=node_size,
                               )
        nx.draw_networkx_edges(graph, pos=spring_pos, width=edge_width)

    nx.draw_networkx_nodes(graph, spring_pos, node_color=node_colours, node_size=node_size,
                           ax=graph_plot)
    nx.draw_networkx_edges(graph, pos=spring_pos, width=edge_width, ax=graph_plot)


def draw_node_and_neighbours(graph: nx.Graph, graph_plot: Axes,
                             selected_node_name: str,
                             num_nodes_to_render=DEFAULT_NODES_TO_RENDER) -> None:
    """ Draw node selected_node_name and it's neighbours on graph_plot. Note that this doesn't
    mean the nodes are visible, as the graph_plot must be rendered outside this function.

    """
    nodes = [selected_node_name]
    edges = []
    neighbours_rendered = 0
    print(
        f'{selected_node_name} has a partisanship score of {graph.nodes[selected_node_name]["bias"]}')
    for neighbour in graph.neighbors(selected_node_name):
        if num_nodes_to_render <= neighbours_rendered:
            print('breaking')
            break
        print(
            f'Neighbour:{neighbour} has a partisanship score of: {graph.nodes[neighbour]["bias"]}')
        nodes.append(neighbour)
        edges.append((selected_node_name, neighbour))
        neighbours_rendered += 1

    node_colours = [get_colour(graph.nodes[node_name]['bias']) for node_name in nodes]
    labels = {}
    for node in nodes:
        labels[node] = node
    # https://networkx.org/documentation/latest/reference/generated/networkx.drawing.layout.spring_layout.html
    spring_pos = nx.spring_layout(nodes)
    nx.draw_networkx_nodes(graph, spring_pos, nodelist=nodes, node_color=node_colours,
                           ax=graph_plot, vmin=PARTISANSHIP_RANGE[0],
                           vmax=PARTISANSHIP_RANGE[1])
    nx.draw_networkx_labels(graph, spring_pos, labels=labels, ax=graph_plot)
    nx.draw_networkx_edges(graph, pos=spring_pos, edgelist=edges, ax=graph_plot)


def draw_limited_num_of_nodes(graph: nx.Graph, graph_plot: Axes,
                              num_nodes=DEFAULT_NODES_TO_RENDER) -> None:
    """ Draw num_nodes nodes, prioritizing connected nodes when
    possible on graph_plot. Note that this doesn't mean the nodes are visible, as the graph_plot
    must be rendered outside this function.

    """

    nodes = []
    edges = []
    original_num_nodes = num_nodes  # TODO: delete this & other debugging stuff
    print('starting converting to set')
    unvisited_nodes = set(graph.nodes)
    print('finished converting to set')
    while num_nodes > 0:
        start_node = unvisited_nodes.pop()
        nodes_clump, edges_clump = _get_nodes_and_edges(graph, start_node, num_nodes, set())
        num_nodes -= len(nodes_clump)
        nodes.extend(nodes_clump)
        edges.extend(edges_clump)
        for node in nodes_clump:
            if node != start_node:
                unvisited_nodes.remove(node)
    if len(nodes) != original_num_nodes:
        print('Wrong # of nodes')

    node_colours = [get_colour(graph.nodes[node_name]['bias']) for node_name in nodes]

    # Color map stuff: https://stackoverflow.com/questions/25748182/python-making-color-bar-that-runs-from-red-to-blue
    labels = {}
    for node in nodes:
        labels[node] = node
    # https://networkx.org/documentation/latest/reference/generated/networkx.drawing.layout.spring_layout.html
    spring_pos = nx.spring_layout(nodes)
    nx.draw_networkx_nodes(graph, spring_pos, nodelist=nodes, node_color=node_colours,
                           ax=graph_plot, vmin=PARTISANSHIP_RANGE[0],
                           vmax=PARTISANSHIP_RANGE[1])
    nx.draw_networkx_labels(graph, spring_pos, labels=labels, ax=graph_plot)
    nx.draw_networkx_edges(graph, pos=spring_pos, edgelist=edges, ax=graph_plot)


def _get_nodes_and_edges(graph: nx.Graph, current_node_name: str, num_nodes: int,
                         visited: set[str]) -> \
        Tuple[List[str], List[Tuple[str, str]]]:
    """ returns tuple of list of num_nodes nodes, and a list of the edges between them.
    Note: The first element of the tuple contains the nodes, and the second element of the tuple
    is the list of edges
    """
    if num_nodes == 0:
        return ([], [])
    else:
        nodes = [current_node_name]
        edges = []
        visited.add(current_node_name)
        for neighbour in graph.neighbors(current_node_name):
            if neighbour not in visited:
                neighbour_nodes, neighbours_edges = _get_nodes_and_edges(graph, neighbour,
                                                                         num_nodes - 1, visited)
                if len(neighbour_nodes) > 0:
                    edges.append((current_node_name, neighbour))
                num_nodes -= len(neighbour_nodes)
                nodes.extend(neighbour_nodes)
                edges.extend(neighbours_edges)
        return (nodes, edges)

    # This should be really similar to a graph traversal algorithm?
    # Should make list "nodelist", which we pass to the draw method
    # also make list "edgelist" that we pass to draw method


def partisanship_score_to_str(partisanship_score: int) -> str:
    ''' Return a partisanship rating from the following list:
    ["Far-Left", "Center-Left", "Moderate", "Center-Right", "Far-Right"] based on the
    partisanship score

    '''
    if PARTISANSHIP_RANGE[0] <= partisanship_score < 0.2:
        return "Far-Left"
    elif 0.2 <= partisanship_score < 0.4:
        return "Center-Left"
    elif 0.4 <= partisanship_score < 0.6:
        return "Moderate"
    elif 0.6 <= partisanship_score < 0.8:
        return "Center-Right"
    else:
        # partisanship score is in [0.8, 1]
        return "Far-Right"


def get_colour(partisanship_score: int) -> str:
    ''' Returns a string representing a colour based on the partisanship score

    '''
    if PARTISANSHIP_RANGE[0] <= partisanship_score < 0.2:
        return 'blue'
    elif 0.2 <= partisanship_score < 0.4:
        return '#0AD6F1'
    elif 0.4 <= partisanship_score < 0.6:
        return '#8A0676'
    elif 0.6 <= partisanship_score < 0.8:
        return '#FF9112'
    else:
        # partisanship score is in [0.8, 1]
        return 'red'


def render_tkinter_gui(graph: nx.Graph, graph_figure: plt.Figure) -> None:
    """ Renders the graph stored in the graph variable, along with UI elements.

    """
    window = tk.Tk()

    frame_graph = tk.Frame(master=window, width=500)
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
    num_nodes_as_str = tk.StringVar(value=str(DEFAULT_NODES_TO_RENDER))

    node_selector = ttk.Combobox(master=frame_user_interaction,
                                 textvariable=selected_node_name)
    partisanship_label = ttk.Label(master=frame_user_interaction)

    # add label for Number of nodes to show
    num_nodes_label = ttk.Label(master=frame_user_interaction, text='Number of nodes to display:')
    # add entry for number of nodes to show
    num_nodes_entry = tk.Entry(master=frame_user_interaction, textvariable=num_nodes_as_str)
    node_selector_label = ttk.Label(master=frame_user_interaction, text='Show neighbours for: ')

    # change logic in on_combobox_selected so it only shows number of nodes neighbours max
    def on_random_nodes_btn_pressed() -> None:
        graph_plot = graph_figure.get_axes()[0]
        graph_plot.clear()
        num_nodes = int(num_nodes_as_str.get())
        draw_limited_num_of_nodes(graph, graph_plot, num_nodes)
        canvas.draw()

    def on_combobox_selected(event: tk.Event) -> None:
        print("combobox selected")
        selected_node_partisanship = partisanship_score_to_str(
            graph.nodes[selected_node_name.get()]['bias'])
        partisanship_label[
            'text'] = f'{selected_node_name.get()} is a {selected_node_partisanship} tweet'

        graph_plot = graph_figure.get_axes()[0]
        graph_plot.clear()
        num_nodes = int(num_nodes_as_str.get())
        print("calling draw_node_and_neighbours")
        draw_node_and_neighbours(graph, graph_plot, selected_node_name.get(), num_nodes)
        print('done with draw_node_and_neighbours')
        canvas.draw()

    # add button for show random nodes
    show_random_nodes_btn = tk.Button(master=frame_user_interaction, text="View random nodes",
                                      command=on_random_nodes_btn_pressed)

    node_selector['values'] = list(graph.nodes)
    node_selector.state(['readonly'])
    node_selector.bind("<<ComboboxSelected>>", on_combobox_selected)

    node_selector.grid(row=0, column=1)
    node_selector_label.grid(row=0, column=0)
    # put an entry to the left of node_selector to explain what it does
    num_nodes_label.grid(row=1, column=0)
    num_nodes_entry.grid(row=1, column=1)
    show_random_nodes_btn.grid(row=2, column=0)
    partisanship_label.grid(row=2, column=1)

    window.mainloop()


def visualize_whole_graph(graph_nx: nx.Graph,
                          layout: str = 'spring_layout') -> None:
    """Use plotly and networkx to visualize the given graph.

    NOTE: This is a modified version of visualize_graph from a3_visualization.py
    Optional arguments:
        - layout: which graph layout algorithm to use
    """

    LINE_COLOUR = 'rgb(210,210,210)'
    VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    node_colours = [get_colour(graph_nx.nodes[node_name]['bias']) for node_name in graph_nx.nodes]

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=LINE_COLOUR, width=1),
                     hoverinfo='none',
                     )
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 color=node_colours,
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data1 = [trace3, trace4]
    fig = Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.show()


if __name__ == '__main__':
    # https://stackoverflow.com/questions/20133479/how-to-draw-directed-graphs-using-networkx-in-python
    import csv_to_graph

    g = csv_to_graph.load_weighted_hashtags_graph('total_filtered_politician.csv')
    csv_to_graph.add_edges('total_filtered_politician.csv', g)
    nx_graph = g.to_networkx()
    # nx_graph = generate_dummy_graph(50)
    print('converted to networkx')
    figure = plt.Figure()
    subplot = figure.add_subplot(111)

    visualize_whole_graph(nx_graph)

    # render_tkinter_gui(nx_graph, figure)

    import python_ta

    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['python_ta.contracts', 'networkx', 'matplotlib', 'matplotlib.axes',
    #                       'matplotlib.pyplot', 'matplotlib.colors',
    #                       'matplotlib.backends.backend_tkagg', 'tkinter', 'random'],
    #     'disable': ['R1705', 'C0200'],
    # })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    # TODO:
    # https://stackoverflow.com/questions/55553845/display-networkx-graph-inside-the-tkinter-window
    # make it so it doesn't recalculate color when u open a new graph lol
    # Make it so it shows properties when you hover over a node
    #   - https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
    #   - ideally, it would just show up in the side bar

    # NOTE: Jeremy, this is your stuff
    # Why does the application glitch when the mouse is in the boundaries?
    #   - glitching only happens in pan mode, when the graph is in tkinter.
    #   - is this just networkX? Or anything through matplotlib
    #   - Does this happen when you render the whole graph?

    # Tkinter: https://realpython.com/python-gui-tkinter/
    # TODO: maybe refactor so all the tkinter stuff is in a class? May be easier to interact with then
