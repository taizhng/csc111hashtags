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
import rendering
from making_new_csv import get_us_hashtags

# This file convert the processed csv data to python graph datatype
import csv_to_graph

# This file does the visual
from rendering import render_tkinter_gui

if __name__ == '__main__':
    # How we processed the data (Here are few different file size for you to try)
    # uncomment one of the following versions to test our program that process the raw data
    # You don't have to do all of them. Pick one if interested

    # small testing version
    # get_us_hashtags('test_tweet_ids.jsonl', 'full_member_info.csv', 'accounts-twitter-data.csv',
    # 'test_filtered_politician.csv')

    # bigger testing version (It takes 2-3 minutes for me, about one million tweets)
    # get_us_hashtags('small_tweet_ids.jsonl', 'full_member_info.csv', 'accounts-twitter-data.csv',
    # 'small_filtered_politician.csv')

    # This is the dataset we used (warning the following line may take a long time to run,
    # the full version has over 10 million tweets)
    # get_us_hashtags('all_tweet_ids.jsonl', 'full_member_info.csv', 'accounts-twitter-data.csv',
    # 'total_filtered_politician.csv')

    # creates a weighted python graph
    g = csv_to_graph.load_weighted_hashtags_graph('total_filtered_politician.csv', 200)

    nx_graph = g.to_networkx()
    rendering.visualize_graph(nx_graph, "All Hashtags and Their Connections")

    # final graphics output
    render_tkinter_gui(nx_graph)
