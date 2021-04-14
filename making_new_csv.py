"""
A file to filter out all the American politician hashtags into a csv file
"""
import json
import csv


def get_us_hashtags(tweets_file: str, member_info_file: str) -> int:
    """
    This function will create a csv file with only us politicians and their partisan
    scores(democrat: 0, republicans: 1).It returns a integer value of how many politicians that is
    in the original tweet file that are not us politicians or their tweets don't have hashtags.
    """
    # creates a integer to measure the tweets that don't fulfill the requirements.
    unread = 0
    us_politicians = get_us_information(member_info_file)
    # create up a csv file called total_filtered_politician.csv
    # (there is no need to create this file before hand)
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
                # this makes sure that there won't be any empty hashtags
                if tweet['entities']['hashtags'] != []:
                    if user['name'] in us_politicians:
                        writer.writerow(
                            {'name': user['name'],
                             'partisan_score': us_politicians[user['name']],
                             'hashtags': {x['text'] for x in tweet['entities']['hashtags']}})
                    else:
                        unread += 1
            return unread


def get_us_information(file: str) -> dict[str, int]:
    """
    This function will get all us politician's information
    """
    with open(file, encoding="UTF-8") as file_read:
        reader = csv.reader(file_read)
        next(reader)
        data = {}
        for row in reader:
            # filters us politicians and assign their party with score of 0 or 1 to them.
            if row[9] == 'United States':
                if row[4] == 'Democrat':
                    data[row[0]] = 0
                elif row[4] == 'Republican':
                    data[row[0]] = 1
    return data


if __name__ == '__main__':
    # this out put a csv file from the two given file
    get_us_hashtags('all_tweet_ids.jsonl', 'full_member_info.csv')
