import random
from typing import List, Tuple

import networkx as nx
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk

partisanship_range = [0, 1]
DEFAULT_NODES_TO_RENDER = 50


def generate_dummy_graph(num_nodes: int) -> nx.Graph:
    """
    Creates a weighted graph, in order to test GUI

    """
    g = nx.Graph()
    threshold_for_edge = 0.5

    for i in range(num_nodes):
        partisanship = random.uniform(partisanship_range[0], partisanship_range[1])

        node_name = f'Node {i}'
        g.add_node(node_name, partisanship=partisanship)
    for i in range(num_nodes):
        node_name = f'Node {i}'
        if random.random() > threshold_for_edge:
            connected_node_name = f'Node {random.randrange(0, num_nodes)}'
            g.add_edge(node_name, connected_node_name)

    return g


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
        f'{selected_node_name} has a partisanship score of {g.nodes[selected_node_name]["partisanship"]}')
    for neighbour in graph.neighbors(selected_node_name):
        if (num_nodes_to_render <= neighbours_rendered):
            print('breaking')
            break
        print(f'{selected_node_name} is neighbour to {neighbour}')
        print(f'{neighbour} has a partisanship score of: {g.nodes[neighbour]["partisanship"]}')
        nodes.append(neighbour)
        edges.append((selected_node_name, neighbour))
        neighbours_rendered += 1

    blue_to_red = colors.LinearSegmentedColormap.from_list("BlueToRed", ["b", "r"])
    node_colours = [graph.nodes[node_name]['partisanship'] for node_name in nodes]
    # TODO: iron out bug where the colour of node changes for this vs what it originally was
    nx.draw(g, cmap=blue_to_red, node_color=node_colours, nodelist=nodes, edgelist=edges,
            with_labels=True, ax=graph_plot)


def draw_limited_num_of_nodes(graph: nx.Graph, graph_plot: Axes, num_nodes: int):
    """ Draw num_nodes nodes, choosing nodes randomly, but prioritizing connected nodes when
    possible on graph_plot. Note that this doesn't mean the nodes are visible, as the graph_plot
    must be rendered outside this function.

    """

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

    node_colours = [g.nodes[node_name]['partisanship'] for node_name in nodes]

    # Color map stuff: https://stackoverflow.com/questions/25748182/python-making-color-bar-that-runs-from-red-to-blue
    blue_to_red = colors.LinearSegmentedColormap.from_list("BlueToRed", ["b", "r"])
    labels = {}
    for node in nodes:
        labels[node] = node
    nx.draw_networkx_nodes(g, spring_pos, nodelist=nodes, node_color=node_colours,
                           cmap=blue_to_red, ax=a)
    nx.draw_networkx_labels(g, spring_pos, labels=labels, ax=a)
    nx.draw_networkx_edges(g, pos=spring_pos, edgelist=edges, ax=a)


def _get_nodes_and_edges(graph: nx.Graph, current_node_name: str, num_nodes: int,
                         visited: set[str]) -> \
        Tuple[List[str], List[Tuple[str, str]]]:
    """ returns tuple of list of num_nodes nodes, and a list of the edges between them.
    Note: The first element of the tuple contains the nodes, and the second element of the tuple
    is the list of edges
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


def partisanship_score_to_str(partisanship_score: int) -> str:
    ''' Return a partisanship rating from the following list:
    ["Far-Left", "Center-Left", "Moderate", "Center-Right", "Far-Right"] based on the
    partisanship score

    '''
    if partisanship_range[0] <= partisanship_score < 0.2:
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
    def on_random_nodes_btn_pressed():
        graph_plot = graph_figure.get_axes()[0]
        graph_plot.clear()
        num_nodes = int(num_nodes_as_str.get())
        draw_limited_num_of_nodes(graph, graph_plot, num_nodes)
        canvas.draw()

    def on_combobox_selected(event):
        selected_node_partisanship = partisanship_score_to_str(
            graph.nodes[selected_node_name.get()]['partisanship'])
        partisanship_label[
            'text'] = f'{selected_node_name.get()} is a {selected_node_partisanship} tweet'

        graph_plot = graph_figure.get_axes()[0]
        graph_plot.clear()
        num_nodes = int(num_nodes_as_str.get())
        draw_node_and_neighbours(graph, graph_plot, selected_node_name.get(), num_nodes)
        canvas.draw()

    # add button for show random nodes
    show_random_nodes_btn = tk.Button(master=frame_user_interaction, text="View random nodes",
                                      command=on_random_nodes_btn_pressed)

    node_selector['values'] = nodes_list
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


if __name__ == '__main__':
    # https://stackoverflow.com/questions/20133479/how-to-draw-directed-graphs-using-networkx-in-python
    g = generate_dummy_graph(50)
    num_nodes = 7
    graph_figure = plt.Figure()
    a = graph_figure.add_subplot(111)
    spring_pos = nx.spring_layout(g)
    node_colours = [g.nodes[node_name]['partisanship'] for node_name in g.nodes()]

    # Color map stuff: https://stackoverflow.com/questions/25748183/python-making-color-bar-that-runs-from-red-to-blue
    blue_to_red = colors.LinearSegmentedColormap.from_list("BlueToRed", ["b", "r"])
    nx.draw(g, cmap=blue_to_red, node_color=node_colours, with_labels=True, ax=a)

    render_tkinter_gui(g, graph_figure, list(g.nodes))

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
