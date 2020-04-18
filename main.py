import datetime

import Guardian
from Day import Day
from Topic import Topic

from General import Functions


def get_day_list(article_folder_path):
    day_list = []
    for json_path in Functions.get_path_list_from_directory(article_folder_path):
        day_list.append(Day(json_path))
    return day_list


def get_topic_list():
    return [
        Topic(name="tech", keyword_list=["apple", "iphone", "android", "phone"]),
        # Topic(name="", keyword_list=[]),
        # Topic(name="", keyword_list=[]),
        # Topic(name="", keyword_list=[]),
        # Topic(name="", keyword_list=[]),
        # Topic(name="", keyword_list=[]),
        # Topic(name="", keyword_list=[]),
        # Topic(name="", keyword_list=[]),
        # Topic(name="", keyword_list=[]),
        Topic(name="covid-19", keyword_list=["covid-19", "coronavirus", "virus", "pandemic"])
    ]


def main():

    article_folder_path = "Day JSON Folder"

    do_download = False
    if do_download:
        Guardian.get_articles(
            folder_path=article_folder_path,
            start_date=datetime.date(2019, 10, 1),
            end_date=datetime.date(2020, 4, 10)
        )

    day_list = get_day_list(article_folder_path=article_folder_path)

    # article_count = 0
    # for day in day_list:
    #     print(day)
    #     article_count += day.article_count
    # print(article_count)

    topic_list = get_topic_list()

    for topic in topic_list:
        topic.update_day_freq_dict(day_list)

    for topic in topic_list:
        print(topic)


main()
