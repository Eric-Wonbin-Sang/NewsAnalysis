import os
import datetime
import json
import requests
import nltk
nltk.downloader.download('vader_lexicon')

article_folder_path = "Day JSON Folder"


class Article:

    def __init__(self, date, data_dict):
        self.data_dict = data_dict

        self.date = date
        self.headline = self.get_headline()
        self.text = self.get_text()

    def get_headline(self):
        return self.data_dict["webTitle"]

    def get_text(self):
        return self.data_dict["fields"]["bodyText"]

    def get_freq_of_keywords(self, keyword_list):
        header_word_list = self.headline.lower().replace(".", " ").replace(",", " ").split(" ")
        text_word_list = self.text.lower().replace(".", " ").replace(",", " ").split(" ")
        final_word_list = header_word_list + text_word_list
        freq = 0
        for word in final_word_list:
            if word in keyword_list:
                freq += 1
        return freq

    def __str__(self):
        ret_str = "Date: {}\t".format(self.date.strftime("%Y-%m-%d"))
        ret_str += "Headline: {}\t".format(self.headline[:20] + "...")
        ret_str += "Text: {}".format(self.text[:20] + "...")
        return ret_str


class Day:

    def __init__(self, json_path):
        self.json_path = json_path

        self.date = self.get_date()

        self.article_list = self.get_article_list()

    def get_date(self):  # returns a datetime object from the datetime library
        date_str = self.json_path.split("\\")[-1].split("/")[-1].split(".")[0]
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")

    def get_article_list(self):
        with open(self.json_path) as json_file:  # json_file is a json object
            print("\tGetting article_list from", self.json_path)
            data_dict_list = json.load(json_file)

        article_list = []
        for data_dict in data_dict_list:
            article_list.append(Article(date=self.date, data_dict=data_dict))
        return article_list

    def __str__(self):
        ret_str = "Date: " + self.date.strftime('%Y-%m-%d') + "\t"
        ret_str += "json Path: " + self.json_path + "\t"
        ret_str += "Article Count: " + str(len(self.article_list))
        return ret_str


def get_path_list_from_directory(folder_path):
    path_list = []
    for path in os.listdir(folder_path):
        full_path = os.path.join(folder_path, path)
        if os.path.isfile(full_path):
            path_list.append(full_path)
    return path_list


def download_articles(folder_path):
    ARTICLES_DIR = os.path.join(folder_path)
    os.makedirs(ARTICLES_DIR, exist_ok=True)

    MY_API_KEY = "43470979-7aa9-4d5d-84f5-4ad9e9f8ce20"
    API_ENDPOINT = 'http://content.guardianapis.com/search'
    api_params = {
        'from-date': None,  # will be added during for loop
        'to-date': None,  # will be added during for loop
        'order-by': "newest",
        'show-fields': 'all',
        'page-size': 200,
        'api-key': MY_API_KEY
    }

    start_date = datetime.date(2019, 10, 1)
    end_date = datetime.date(2020, 4, 10)

    for day_count in range((end_date - start_date).days + 1):

        curr_datetime = start_date + datetime.timedelta(days=day_count)
        curr_date_str = curr_datetime.strftime('%Y-%m-%d')
        json_path = os.path.join(ARTICLES_DIR, curr_date_str + '.json')

        if not os.path.exists(json_path):

            print("{} - Downloading {}".format(day_count, curr_date_str))

            all_results = []
            api_params['from-date'] = curr_date_str
            api_params['to-date'] = curr_date_str

            current_page = 1
            total_pages = 1
            while current_page <= total_pages:
                print("\t\tpage", current_page)
                api_params['page'] = current_page
                resp = requests.get(API_ENDPOINT, api_params)
                data = resp.json()
                all_results.extend(data['response']['results'])

                current_page += 1
                total_pages = data['response']['pages']

            with open(json_path, 'w') as f:
                print("\tWriting to", json_path)
                f.write(json.dumps(all_results, indent=2))


def get_day_list():
    day_list = []
    for path in get_path_list_from_directory(article_folder_path):
        print("Day path:", path)
        day_list.append(Day(path))
    return day_list


def get_and_print_day_list():
    day_list = get_day_list()

    for i, day in enumerate(day_list):
        for article in day.article_list:
            print("Article {}: {}".format(i + 1, str(article)))
            # this takes some time to run since it's going through all articles each day
    return day_list


day_list = get_day_list()
print("data_collector is finished")

# -------------------------------------------------------


class Topic:

    def __init__(self, name, keyword_list, graph_color):
        self.name = name
        self.keyword_list = keyword_list
        self.graph_color = graph_color
        self.day_freq_dict = {}
        self.article_list = []

    def update_day_freq_dict(self, day_list):
        for day in day_list:
            day_freq = 0
            for article in day.article_list:
                curr_freq = article.get_freq_of_keywords(self.keyword_list)
                if curr_freq > 0:
                    day_freq += curr_freq
                    self.article_list.append(article)
            self.day_freq_dict[day] = day_freq

    def __str__(self):
        ret_str = "Name: " + self.name + "\t"
        ret_str += "Article Count: " + str(len(self.article_list)) + "\t"
        ret_str += "Keywords: " + str(self.keyword_list)
        return ret_str


def get_topic_list():
    print("Creating topic_list")
    topic_list = [
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
    for topic in topic_list:
        print("\tUpdating topic", topic.name)
        topic.update_day_freq_dict(day_list)
    return topic_list


def get_and_print_topic_list():
    topic_list = get_topic_list()

    for topic in topic_list:
        print(topic)

    return topic_list


topic_list = get_and_print_topic_list()
print("topic_creator is finished")

# -------------------------------------------------------

import matplotlib.pyplot
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def make_overall_freq_graph():
    matplotlib.pyplot.figure(figsize=(15, 12))

    for topic in topic_list:
        x = [day_key.date for day_key in topic.day_freq_dict]  # X-axis: dates
        y = [topic.day_freq_dict[day_key] for day_key in topic.day_freq_dict]  # Y-axis: freq

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


def topic_sent_change_over_time():
    sid = SentimentIntensityAnalyzer()

    for topic in topic_list:
        print(topic.name, "-----------------------------------")

        day_sentence_list_dict = {}
        for article in topic.article_list:
            sentence_list = []

    #         this splits up the aritcle body into sentences based on punctuation (., !, ?)
            temp_sentence_list = article.text.split(".")
            new_temp_sentence_list = []
            for temp_sentence in temp_sentence_list:
                new_temp_sentence_list += temp_sentence.split("?")
            temp_sentence_list = new_temp_sentence_list
            new_temp_sentence_list = []
            for temp_sentence in temp_sentence_list:
                new_temp_sentence_list += temp_sentence.split("!")
            temp_sentence_list = new_temp_sentence_list

            for sentence in temp_sentence_list:
                append_cond = False
                for keyword in topic.keyword_list:
                    if keyword in sentence:
                        append_cond = True
                        break
                if append_cond:
                    sentence_list.append(sentence)

            if article.date in day_sentence_list_dict:
                day_sentence_list_dict[article.date] += sentence_list
            else:
                day_sentence_list_dict[article.date] = sentence_list

        date_sent_dict = {}
        for day_key in day_sentence_list_dict:

            sent_list = []

            for sentence in day_sentence_list_dict[day_key]:
                for word in sentence.split(" "):

                    sent = sid.lexicon.get(word)
                    if sent is not None:
                        sent_list.append(sent)

            if len(sent_list) != 0:
                date_sent_dict[day_key] = sum(sent_list) / len(sent_list)  # avg sentiment of the day
            else:
                date_sent_dict[day_key] = 0

        for i, day_key in enumerate(date_sent_dict):
            if i == 3:
                print("\t", day_key, date_sent_dict[day_key], "...")
                break
            else:
                print("\t", day_key, date_sent_dict[day_key])

        fig, (ax1, ax2) = matplotlib.pyplot.subplots(2, 1, figsize=(10, 8))
        fig.suptitle("{} - Date vs Frequency | Date vs Sentiment".format(topic.name))

        ax1.grid()
        ax2.grid()

        ax1.plot([day_key.date for day_key in topic.day_freq_dict],
                 [topic.day_freq_dict[day_key] for day_key in topic.day_freq_dict],
                 color=topic.graph_color)
        ax2.plot([date_key for date_key in date_sent_dict],
                 [date_sent_dict[date_key] for date_key in date_sent_dict],
                 color=topic.graph_color)

        fig.show()


def topic_to_covid_freq_graphs():
    covid_topic = topic_list[0]

    for topic in topic_list[1:]:
        print("Topic: {}".format(topic.name))
        date_covid_hit_dict = {}
        for article in topic.article_list:
            keyword_hit_counter = 0
            for word in article.text.replace(",", " ").split(" "):
                if word in covid_topic.keyword_list:
                    keyword_hit_counter += 1

            if article.date in date_covid_hit_dict:
                date_covid_hit_dict[article.date] += keyword_hit_counter
            else:
                date_covid_hit_dict[article.date] = keyword_hit_counter

        for i, date_key in enumerate(date_covid_hit_dict):
            if i == 3:
                print("\t", date_key, date_covid_hit_dict[date_key], "...")
                break
            else:
                print("\t", date_key, date_covid_hit_dict[date_key])

        matplotlib.pyplot.figure(figsize=(15, 12))

        matplotlib.pyplot.plot(
            [day_key.date for day_key in topic.day_freq_dict],
            [topic.day_freq_dict[day_key] for day_key in topic.day_freq_dict],
            color=topic.graph_color,
            label=topic.name
        )
        matplotlib.pyplot.plot(
            [date_key for date_key in date_covid_hit_dict],
            [date_covid_hit_dict[date_key] for date_key in date_covid_hit_dict],
            color=covid_topic.graph_color,
            label="Coronavirus freq"
        )

        matplotlib.pyplot.gcf().autofmt_xdate()
        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()

# -------------------------------------------------------


print("Function:", "make_overall_freq_graph")
make_overall_freq_graph()

print("Function:", "topic_sent_change_over_time")
topic_sent_change_over_time()

print("Function:", "topic_to_covid_freq_graphs")
topic_to_covid_freq_graphs()
