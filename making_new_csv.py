"""
A file to filter out all the American politician hashtags into a csv file
"""
import json
import csv


# def convert_python_to_csv(tweets_file: str, member_info_file: str) -> None:
#     """
#     This function will convert the results from get_us_hashtags to a csv file
#     """
#     filtered_results = get_us_hashtags(tweets_file, member_info_file)
#     with open('partial_filtered_politician.csv', mode='w') as csv_file:
#         fieldnames = ['name', 'partisan_score', 'hashtags']
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
#         writer.writeheader()
#         for filtered_result in filtered_results:
#             writer.writerow(
#                 {'name': filtered_result['name'],
#                  'partisan_score': filtered_result['partisan_score'],
#                  'hashtags': filtered_result['hashtags']})


def get_us_hashtags(tweets_file: str, member_info_file: str) -> int:
    """
    This function will get rid of all the non us hashtags and return a dictionary with these
    people's name, partisan score(Democrats: 0, Republicans: 1), and hashtags.
    """
    unread = 0
    us_politicians = get_us_information(member_info_file)
    with open('total_filtered_politician.csv', mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['name', 'partisan_score', 'hashtags']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
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


def read_tweets_file_data(file: str) -> list[dict]:
    """Return a list of dictionary values containing the given tweet data file.

    Preconditions:
        - file is the path to a JSON file containing tweet data.
    """
    with open(file, encoding="UTF-8") as json_file:
        data = [json.loads(line) for line in json_file]

    return data


def get_us_information(file: str) -> dict[str, int]:
    """
    This function will get all us politician's information
    """
    with open(file, encoding="UTF-8") as file_read:
        reader = csv.reader(file_read)
        next(reader)
        data = {}
        for row in reader:
            if row[9] == 'United States':
                if row[4] == 'Democrat':
                    data[row[0]] = 0
                elif row[4] == 'Republican':
                    data[row[0]] = 1
    return data


if __name__ == '__main__':
    # this out put a csv file from the two given file
    get_us_hashtags('all_tweet_ids.jsonl', 'full_member_info.csv')
