"""CSC111 Final Assignment Main

Description
===============================
Run this to load our data files and interact with the resulting graphs with a GUI

Copyright and Usage Information
===============================
This file is provided solely for the final assignment of CSC110 at the University of Toronto
St. George campus. All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.
This file is Copyright (c) 2021 Jiajin Wu, Tai Zhang, and Kenneth Miura.
"""
import csv_to_graph
import rendering

if __name__ == '__main__':
    graph = csv_to_graph.load_weighted_hashtags_graph('total_filtered_politician.csv', 200)

    nx_graph = graph.to_networkx()
    rendering.visualize_graph(nx_graph)
    rendering.render_tkinter_gui(nx_graph)
