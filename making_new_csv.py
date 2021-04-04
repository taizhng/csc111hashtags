"""
A file to filter out all the American politician hashtags into a csv file
"""
import json
import csv


def convert_python_to_csv(tweets_file: str, member_info_file: str) -> None:
    """
    This function will convert the results from get_us_hashtags to a csv file
    """
    filtered_results = get_us_hashtags(tweets_file, member_info_file)
    with open('filtered_politician.csv', mode='w') as csv_file:
        fieldnames = ['name', 'partisan_score', 'hashtags']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        for filtered_result in filtered_results:
            writer.writerow(
                {'name': filtered_result['name'],
                 'partisan_score': filtered_result['partisan_score'],
                 'hashtags': filtered_result['hashtags']})


def get_us_hashtags(tweets_file: str, member_info_file: str) -> list[dict]:
    """
    This function will get rid of all the non us hashtags and return a dictionary with these
    people's name, partisan score(Democrats: 0, Republicans: 1), and hashtags.
    """
    us_hashtags = []
    tweets = read_tweets_file_data(tweets_file)
    us_politicians = get_us_information(member_info_file)
    for tweet in tweets:
        for us_politician in us_politicians:
            user = tweet['user']
            # this makes sure that there won't be any empty hashtags
            if us_politician['name'] == user['name'] and tweet['entities']['hashtags'] != []:
                politician_info = {'name': user['name'],
                                   'partisan_score': us_politician['partisan_score'],
                                   'hashtags': {x['text'] for x in tweet['entities']['hashtags']}}
                us_hashtags.append(politician_info)
    return us_hashtags


def read_tweets_file_data(file: str) -> list[dict]:
    """Return a list of dictionary values containing the given tweet data file.

    Preconditions:
        - file is the path to a JSON file containing tweet data.
    """
    with open(file, encoding="UTF-8") as json_file:
        data = [json.loads(line) for line in json_file]

    return data


def get_us_information(file: str) -> list[dict]:
    """
    This function will get all us politician's information
    """
    with open(file, encoding="UTF-8") as file_read:
        reader = csv.reader(file_read)
        next(reader)
        data = []
        for row in reader:
            if row[9] == 'United States':
                politician_info = {'name': row[0]}
                if row[4] == 'Democrat':
                    politician_info['partisan_score'] = 0
                elif row[4] == 'Republican':
                    politician_info['partisan_score'] = 1
                data.append(politician_info)
    return data


if __name__ == '__main__':
    # this out put a csv file from the two given file
    convert_python_to_csv('small_tweet_ids.jsonl', 'full_member_info.csv')
