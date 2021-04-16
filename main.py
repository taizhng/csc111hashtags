"""
CSC111 Winter 2021 Project

This is a file to filter out all the American politician hashtags into a csv file
from hydrated tweet files

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the professors and TAs
in CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this CSC111 project,
please consult with us.

This file is Copyright (c) 2021 Jiajin Wu, Tai Zhang, and Kenneth Miura.
"""
# This file converted the hydrated tweet files to a csv file
from making_new_csv import get_us_hashtags

# This file convert the processed csv data to python graph datatype
import csv_to_graph

# This file does the visual
from rendering import render_tkinter_gui

if __name__ == '__main__':
    # How we processed the data (Here are few different file size for you to try)
    # Just so you know, please run this after testing our full program, as it will overwrite the
    # total_filtered_politician.csv that we gave in the zip file.
    # OR You can uncomment line 36 and comment line 37 in making_new_csv.py.
    # uncomment one of the following versions to test our program that process the raw data

    # small testing version
    # get_us_hashtags('test_tweet_ids.jsonl', 'full_member_info.csv', 'accounts-twitter-data.csv')

    # bigger testing version (It takes 2-3 minutes for me, about one million tweets)
    # get_us_hashtags('small_tweet_ids.jsonl', 'full_member_info.csv', 'accounts-twitter-data.csv')

    # This is the dataset we used (warning the following line may take a while to run,
    # the full version has over 10 million tweets)
    # get_us_hashtags('all_tweet_ids.jsonl', 'full_member_info.csv', 'accounts-twitter-data.csv')

    # creates a weighted python graph
    g = csv_to_graph.load_weighted_hashtags_graph('total_filtered_politician.csv', 200)
    print(f' nodes num: {len(list(g.get_vertices()))}')

    nx_graph = g.to_networkx()
    print(f'post conversion node nums: {len(list(nx_graph.nodes))}')
    print(f'Trump bias: {nx_graph.nodes["Trump"]["bias"]}')
    print('converted to networkx')

    # final graphics output
    render_tkinter_gui(nx_graph)
