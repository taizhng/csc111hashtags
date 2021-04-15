"""
CSC111 2021 Project 1, Part 1 Making New CSV

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
import json
import csv


def get_us_hashtags(tweets_file: str, member_info_file: str, senate_file: str) -> dict[str, int]:
    """
    This function will create a csv file with only us politicians and their partisan
    scores(democrat: 0, republicans: 1).It returns a integer value of how many politicians that is
    in the original tweet file that are not us politicians or their tweets don't have hashtags.
    """
    # creates a integer to measure the tweets that iis not us politician tweets,
    # but still with hashtags in their tweets.
    unread = 0
    # Try to find how many different us politicians send tweets
    unique_politicians = set()
    us_politicians = get_us_information(member_info_file, senate_file)
    # create up a csv file called total_filtered_politician.csv
    # (there is no need to create this file before hand)
    # uncomment the following line for testing if you want.
    # with open('test_filtered_politician.csv', mode='w', encoding='utf-8') as csv_file:
    with open('total_filtered_politician.csv', mode='w', encoding='utf-8') as csv_file:
        # the header for the csv files
        fieldnames = ['name', 'partisan_score', 'hashtags']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        # this opens up the tweet file that we hydrated
        with open(tweets_file, encoding="UTF-8") as json_file:
            print("opened")
            for line in json_file:
                tweet = json.loads(line)
                user = tweet['user']
                user_id = user['id_str']
                # this makes sure that there won't be any empty hashtags
                if tweet['entities']['hashtags'] != []:
                    if user_id in us_politicians:
                        writer.writerow(
                            {'name': user['name'],
                             'partisan_score': us_politicians[user['id_str']],
                             'hashtags': {x['text'] for x in tweet['entities']['hashtags']}})
                        unique_politicians.add(user_id)
                    else:
                        unread += 1
            return {'unread': unread, 'unique_politicians': len(unique_politicians)}


def get_us_information(all_nations_file: str, senate_file: str) -> dict[str, int]:
    """
    This function will get all us politician's information
    """
    senate_info = get_us_senator(senate_file)
    with open(all_nations_file, encoding="UTF-8") as file_read:
        reader = csv.reader(file_read)
        next(reader)
        data = {}
        for row in reader:
            # filters us politicians and assign their party with score of 0 or 1 to them.
            if row[9] == 'United States':
                if row[4] == 'Democrat':
                    data[row[3]] = 0
                elif row[4] == 'Republican':
                    data[row[3]] = 1
        # combines both senate and house of representatives
        data.update(senate_info)
    return data


def get_us_senator(file: str) -> dict[str, int]:
    """
    This function will get the us senator's twitter ids and their partisan score
    This is done, because full_member_ids contains only house of representatives
    """
    with open(file, encoding="UTF-8") as file_read:
        reader = csv.reader(file_read)
        next(reader)
        data = {}
        # Only contains information for the senate
        for row in reader:
            if row[14] == 'Congress':
                if row[15] == 'Democrat':
                    data[row[1]] = 0
                elif row[15] == 'Republican':
                    data[row[1]] = 1
    return data


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['csv', 'json'],
        'allowed-io': ['get_us_information', 'get_us_hashtags', 'get_us_senator'],
        'max-nested-blocks': 4
    })

    # this output a csv file from the three given file

    # testing version (It takes 2-3 minutes for me, I used an old laptop which makes it slow)
    # Just so you know, please run this after testing our full program, as it will overwrite the
    # total_filtered_politician.csv that we gave in the zip file.
    # OR You can uncomment line 36 and comment line 37.
    get_us_hashtags('small_tweet_ids.jsonl', 'full_member_info.csv', 'accounts-twitter-data.csv')

    # (warning the following line may take a while to run,
    # the full version has over 10 million tweets)
    # get_us_hashtags('all_tweet_ids.jsonl', 'full_member_info.csv', 'accounts-twitter-data.csv')
