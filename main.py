import datetime
import matplotlib.pyplot

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
        Topic(
            name="Coronavirus",
            keyword_list=["covid-19", "covid91", "covid", "coronavirus", "virus", "pandemic"],
            graph_color="#ff0000"
        ),
        Topic(
            name="Tech",
            keyword_list=["apple", "iphone", "android", "phone", "tech", "technology", "laptop", "computer"],
            graph_color="#3269a8"
        ),
        Topic(
            name="Finance",
            keyword_list=["bank", "finance", "financial", "earnings", "stock", "performance", "dividends",
                          "shareholders"],
            graph_color="#1fcc21"
        ),
        Topic(
            name="Politics",
            keyword_list=["election", "president", "politics", "trump", "bernie", "biden", "congress", "votes",
                          "voting", "voters", "ballet", "democrat", "republican", "democratic", "conservative"],
            graph_color="#f08f18"
        ),
        Topic(
            name="Entertainment",
            keyword_list=["streaming", "entertainment", "stream", "netflix", "hulu", "disney+", "disney", "movie",
                          "movies", "youtube", "theater"],
            graph_color="#f018a1"
        ),
        Topic(
            name="Sports",
            keyword_list=["football", "basketball", "soccer", "coach", "sports", "season", "sport", "playoff",
                          "playoffs", "fans"],
            graph_color="#f018a1"
        )
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

    for topic in topic_list:
        x = [day_key.date for day_key in topic.day_freq_dict]   # X-axis: dates
        y = [topic.day_freq_dict[day_key] for day_key in topic.day_freq_dict]   # Y-axis: freq

        matplotlib.pyplot.plot(
            x, y,
            # marker='o', markerfacecolor='blue', markersize=12,
            color=topic.graph_color,
            # linewidth=4, linestyle='dashed',
            label=topic.name
        )

    matplotlib.pyplot.gcf().autofmt_xdate()
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()


main()
