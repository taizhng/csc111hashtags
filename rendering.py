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
This file is Copyright (c) 2021 Jiajin Wu, Tai Zhang, and Kenneth Miura.
"""
from typing import List, Tuple
import tkinter as tk
from tkinter import ttk

import networkx as nx

from plotly.graph_objs import Scatter, Figure, Layout
import plotly.graph_objs as go

PARTISANSHIP_RANGE = [0, 1]
DEFAULT_NODES_TO_RENDER = 20
MIN_LINE_WIDTH = 3.0
NODE_SIZE_MULTIPLIER = 10
MAX_LINE_WIDTH = 20
MAX_NODE_SIZE = 100
MIN_NODE_SIZE = 20


def draw_node_and_neighbours(graph: nx.Graph,
                             selected_node_name: str,
                             num_nodes=DEFAULT_NODES_TO_RENDER) -> None:
    """ Draw node selected_node_name and it's neighbours. The graph will be rendered in a new tab
    in the user's browser

    Preconditions:
        - num_nodes > 0

    Optional arguments:
        - num_nodes: The maximum number of nodes that can appear in the graph
    """

    total_nodes = len(list(graph.nodes))
    if num_nodes > total_nodes:
        num_nodes = total_nodes
    node_size = max(MAX_NODE_SIZE / num_nodes, MIN_NODE_SIZE)
    line_width = max(MAX_LINE_WIDTH / num_nodes, MIN_LINE_WIDTH)
    nodes = [(selected_node_name, graph.nodes[selected_node_name])]
    edges = []
    nodes_rendered = 1
    for neighbour in graph.neighbors(selected_node_name):
        if num_nodes <= nodes_rendered:
            break
        nodes.append((neighbour, graph.nodes[neighbour]))
        edge_weight = graph[selected_node_name][neighbour]['weight']
        edges.append((selected_node_name, neighbour, {'weight': edge_weight}))
        nodes_rendered += 1

    new_graph = nx.Graph()
    new_graph.add_nodes_from(nodes)
    new_graph.add_edges_from(edges)
    visualize_graph(new_graph, f"Displaying immediate neighbours of #{selected_node_name}",
                    min_node_size=node_size, line_width=line_width)


def draw_limited_num_of_nodes(graph: nx.Graph,
                              num_nodes=DEFAULT_NODES_TO_RENDER) -> None:
    """ Draw num_nodes nodes from the Object "graph", prioritizing connected nodes when
    possible. Will open the graph in your default browser

    Preconditions:
        - num_nodes > 0
    Optional arguments:
        - num_nodes: The maximum number of nodes that can appear in the graph
    """
    total_nodes = len(list(graph.nodes))
    if num_nodes > total_nodes:
        num_nodes = total_nodes
    node_size = max(MAX_NODE_SIZE / num_nodes, MIN_NODE_SIZE)
    line_width = round(max(MAX_LINE_WIDTH / num_nodes, MIN_LINE_WIDTH))

    original_num_nodes = num_nodes

    nodes = []
    edges = []
    unvisited_nodes = set(graph.nodes)
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
    new_graph = nx.Graph()
    new_graph.add_nodes_from(nodes)
    new_graph.add_edges_from(edges)

    visualize_graph(new_graph, title=f"Displaying {original_num_nodes} random nodes",
                    min_node_size=node_size, line_width=line_width)


def _get_nodes_and_edges(graph: nx.Graph, current_node_name: str, num_nodes: int,
                         visited: set[str]) -> \
        Tuple[List[str], List[Tuple[str, str]]]:
    """ returns tuple of list of num_nodes nodes from the graph, and a list of the edges between them.
    Note: The first element of the tuple contains the nodes, and the second element of the tuple
    is the list of edges

    The visited parameter represents nodes that were already visited by this recursive algorithm


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


def partisanship_score_to_str(partisanship_score: int) -> str:
    ''' Return a partisanship rating from the following list:
    ["Far-Left", "Center-Left", "Moderate", "Center-Right", "Far-Right"] based on the
    partisanship score

    '''
    if PARTISANSHIP_RANGE[0] <= partisanship_score < 0.2:
        return "Extremely Democratic"
    elif 0.2 <= partisanship_score < 0.4:
        return "Moderately Democratic"
    elif 0.4 <= partisanship_score < 0.6:
        return "Moderate"
    elif 0.6 <= partisanship_score < 0.8:
        return "Moderately Republican"
    else:
        # partisanship score is in [0.8, 1]
        return "Extremely Republican"


def get_colour(partisanship_score: int) -> str:
    ''' Returns a string representing a colour based on the partisanship score. It will either
    be in the form of the colours name (i.e. "blue"), or a hexadecimal code

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
    num_nodes_label = ttk.Label(master=frame_user_interaction,
                                text='Number of vertices to display:')
    # add entry for number of nodes to show
    num_nodes_entry = tk.Entry(master=frame_user_interaction, textvariable=num_nodes_as_str)
    node_selector_label = ttk.Label(master=frame_user_interaction,
                                    text='Show neighbours for the hashtag: ')

    def on_random_nodes_btn_pressed() -> None:
        if num_nodes_as_str.get() != '' and int(num_nodes_as_str.get()) > 0:
            # Handling the case where there is nothing in the entry box for number of nodes
            num_nodes = int(num_nodes_as_str.get())
        else:
            num_nodes = 1
            num_nodes_as_str.set(1)

        draw_limited_num_of_nodes(graph, num_nodes)

    def on_combobox_selected(event: tk.Event) -> None:
        selected_node_partisanship = partisanship_score_to_str(
            graph.nodes[selected_node_name.get()]['bias'])
        partisanship_label[
            'text'] = f'{selected_node_name.get()} is a {selected_node_partisanship} hashtag'

        if num_nodes_as_str.get() != '' and int(num_nodes_as_str.get()) > 0:
            # Handling the case where there is nothing in the entry box for number of nodes
            num_nodes = int(num_nodes_as_str.get())
        else:
            num_nodes_as_str.set(1)
            num_nodes = 1
        draw_node_and_neighbours(graph, selected_node_name.get(), num_nodes)

    # add button for show random nodes
    show_random_nodes_btn = tk.Button(master=frame_user_interaction, text="View random vertices",
                                      command=on_random_nodes_btn_pressed)

    node_selector['values'] = list(graph.nodes)
    node_selector.state(['readonly'])
    node_selector.bind("<<ComboboxSelected>>", on_combobox_selected)

    node_selector.grid(row=0, column=1)
    node_selector_label.grid(row=0, column=0)
    num_nodes_label.grid(row=1, column=0)
    num_nodes_entry.grid(row=1, column=1)
    show_random_nodes_btn.grid(row=2, column=0)
    partisanship_label.grid(row=2, column=1)

    window.mainloop()


def visualize_graph(graph_nx: nx.Graph, title: str, min_node_size=5.0,
                    line_width=MIN_LINE_WIDTH) -> None:
    """Use plotly and networkx to visualize all edges and nodes from nodes_list. Nodes will be
    rendered with a size of at least min_node_size, and an edge width of at least line_width. the
    graph will have the variable title as it's title

    NOTE: This is a modified version of visualize_graph from a3_visualization.py

    """

    LINE_COLOUR = 'rgb(210,210,210)'
    VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'

    pos = nx.spring_layout(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]

    node_names = list(graph_nx.nodes)

    node_counts = [graph_nx.nodes[node_name]['count'] for node_name in node_names]
    max_count = max(node_counts)
    sizes = [min_node_size + (graph_nx.nodes[node_name]['count'] / max_count) * 30 for node_name
             in node_names]
    node_colours = [get_colour(graph_nx.nodes[node_name]['bias']) for node_name in graph_nx.nodes]

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    labels = []
    for node_name in graph_nx.nodes:
        partisanship = partisanship_score_to_str(graph_nx.nodes[node_name]['bias'])
        count = graph_nx.nodes[node_name]['count']
        labels.append(f'#{node_name} occurs {count} times and is a {partisanship} hashtag')
    edges_scatter = Scatter(x=x_edges,
                            y=y_edges,
                            mode='lines',
                            name='edges',
                            line=dict(color=LINE_COLOUR, width=line_width),
                            hoverinfo='none',
                            )
    edges_traces = Scatter(x=x_values,
                           y=y_values,
                           mode='markers',
                           name='nodes',
                           marker=dict(symbol='circle-dot',
                                       size=sizes,
                                       color=node_colours,
                                       line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                       ),
                           text=labels,
                           hovertemplate='%{text}',
                           hoverlabel={'namelength': 0}
                           )

    data = [edges_scatter, edges_traces]
    fig = Figure(data=data, layout=Layout(
        title=go.layout.Title(text=title)
    ))
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'networkx', 'plotly.graph_obs', 'tkinter'],
        'disable': ['R1705', 'C0200'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
