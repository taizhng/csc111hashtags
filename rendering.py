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

from plotly.graph_objs import Scatter, Figure

PARTISANSHIP_RANGE = [0, 1]
DEFAULT_NODES_TO_RENDER = 20
MIN_NODE_SIZE = 5
MIN_LINE_WIDTH = 3
MAX_NODE_SIZE = 300
MAX_LINE_WIDTH = 20


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


def draw_node_and_neighbours(graph: nx.Graph,
                             selected_node_name: str,
                             num_nodes=DEFAULT_NODES_TO_RENDER) -> None:
    """ Draw node selected_node_name and it's neighbours on graph_plot. Note that this doesn't
    mean the nodes are visible, as the graph_plot must be rendered outside this function.

    Preconditions:
        - num_nodes > 0

    """

    print(f'maximum number of nodes is {len(list(graph.nodes))}')
    node_size = round(max(MAX_NODE_SIZE / num_nodes, MIN_NODE_SIZE))
    line_width = round(max(MAX_LINE_WIDTH / num_nodes, MIN_LINE_WIDTH))
    nodes = [(selected_node_name, graph.nodes[selected_node_name])]
    edges = []
    nodes_rendered = 1
    print(
        f'{selected_node_name} has a partisanship score of {graph.nodes[selected_node_name]["bias"]}')
    for neighbour in graph.neighbors(selected_node_name):
        if num_nodes <= nodes_rendered:
            print('breaking')
            break
        print(
            f'Neighbour:{neighbour} has a partisanship score of: {graph.nodes[neighbour]["bias"]}')
        nodes.append((neighbour, graph.nodes[neighbour]))
        edge_weight = graph[selected_node_name][neighbour]['weight']
        edges.append((selected_node_name, neighbour, {'weight': edge_weight}))
        nodes_rendered += 1

    new_graph = nx.Graph()
    print('adding nodes')
    new_graph.add_nodes_from(nodes)
    print('adding edges')
    new_graph.add_edges_from(edges)
    print('visualizing graph')
    import time
    start = time.time()
    visualize_graph(new_graph, node_size=node_size, line_width=line_width)
    end = time.time()
    print(f'Visualization time: {end - start} seconds')


def draw_limited_num_of_nodes(graph: nx.Graph,
                              num_nodes=DEFAULT_NODES_TO_RENDER) -> None:
    """ Draw num_nodes nodes, prioritizing connected nodes when
    possible. Will open the graph in your default browser

    Preconditions:
        - num_nodes > 0
    """
    node_size = round(max(MAX_NODE_SIZE / num_nodes, MIN_NODE_SIZE))
    line_width = round(max(MAX_LINE_WIDTH / num_nodes, MIN_LINE_WIDTH))

    print(f'maximum number of nodes is {len(list(graph.nodes))}')
    original_num_nodes = num_nodes

    nodes = []
    edges = []
    print('starting converting to set')
    unvisited_nodes = set(graph.nodes)
    print('finished converting to set')
    while num_nodes > 0:
        start_node = unvisited_nodes.pop()
        nodes_clump, edges_clump = _get_nodes_and_edges(graph, start_node, num_nodes, set())
        num_nodes -= len(nodes_clump)
        for node in nodes_clump:
            nodes.append((node, graph.nodes[node]))
            if node != start_node:
                unvisited_nodes.remove(node)
        for edge in edges_clump:
            edge_weight = graph[edge[0]][edge[1]]['weight']
            edges.append((edge[0], edge[1], {'weight': edge_weight}))
    print(f'Nodes drawn: {len(nodes)}: Nodes requested: {original_num_nodes}')
    new_graph = nx.Graph()
    new_graph.add_nodes_from(nodes)
    new_graph.add_edges_from(edges)

    visualize_graph(new_graph, node_size=node_size, line_width=line_width)


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


def render_tkinter_gui(graph: nx.Graph) -> None:
    """ Renders a UI to interact with the graph. Note that all graphs launched will show in a
    new tab in the user's default browser

    """
    window = tk.Tk()
    window.title("Hashtag Partisanship")

    frame_user_interaction = tk.Frame(master=window)
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
        if num_nodes_as_str.get() != '' and int(num_nodes_as_str.get()) > 0:
            # Handling the case where there is nothing in the entry box for number of nodes
            num_nodes = int(num_nodes_as_str.get())
        else:
            num_nodes = 1
            num_nodes_as_str.set(1)

        print(f'num nodes is {num_nodes}')
        draw_limited_num_of_nodes(graph, num_nodes)

    def on_combobox_selected(event: tk.Event) -> None:
        print("combobox selected")
        selected_node_partisanship = partisanship_score_to_str(
            graph.nodes[selected_node_name.get()]['bias'])
        partisanship_label[
            'text'] = f'{selected_node_name.get()} is a {selected_node_partisanship} tweet'

        if num_nodes_as_str.get() != '' and int(num_nodes_as_str.get()) > 0:
            # Handling the case where there is nothing in the entry box for number of nodes
            num_nodes = int(num_nodes_as_str.get())
        else:
            num_nodes_as_str.set(1)
            num_nodes = 1
        print("calling draw_node_and_neighbours")
        draw_node_and_neighbours(graph, selected_node_name.get(), num_nodes)
        print('done with draw_node_and_neighbours')

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


def visualize_graph(graph_nx: nx.Graph, node_size=MIN_NODE_SIZE,
                    line_width=MIN_LINE_WIDTH) -> None:
    """Use plotly and networkx to visualize all edges and nodes from nodes_list

    NOTE: This is a modified version of visualize_graph from a3_visualization.py
    Optional arguments:
        - layout: which graph layout algorithm to use
    """

    LINE_COLOUR = 'rgb(210,210,210)'
    VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'

    # make sure to plug the weights in
    # applying spring_layout to nodes_list when nodes_list is the entire nodes_list is
    # different from giving it the graph
    # pos = nx.spring_layout(nodes_list, weight=None)
    pos = nx.spring_layout(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]

    node_names = list(graph_nx.nodes)
    sizes = [node_size] * len(node_names)
    node_colours = [get_colour(graph_nx.nodes[node_name]['bias']) for node_name in graph_nx.nodes]

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]
    # coloring edges: https://github.com/plotly/plotly.py/issues/591#issuecomment-430187163

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=LINE_COLOUR, width=line_width),
                     hoverinfo='none',
                     )
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=sizes,
                                 color=node_colours,
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=list(graph_nx.nodes),
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
    print(f'pre-removal nodes num: {len(list(g.get_vertices()))}')
    g.remove_min_count(40)
    print(f'post-removal nodes num: {len(list(g.get_vertices()))}')

    nx_graph = g.to_networkx()
    print(f'post conversion node nums: {len(list(nx_graph.nodes))}')
    print(f'Trump bias: {nx_graph.nodes["Trump"]["bias"]}')
    # nx_graph = generate_dummy_graph(50)
    print('converted to networkx')

    # visualize_graph(nx_graph, list(nx_graph.nodes), list(nx_graph.edges))
    render_tkinter_gui(nx_graph)

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
