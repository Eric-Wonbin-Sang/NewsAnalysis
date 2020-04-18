
class Article:

    def __init__(self, day,  data_dict):

        self.data_dict = data_dict

        self.day = day
        self.headline = self.get_headline()
        self.text = self.get_text()

    def get_date(self):
        return self.data_dict["webPublicationDate"]

    def get_headline(self):
        return self.data_dict["webTitle"]

    def get_text(self):
        return self.data_dict["fields"]["bodyText"]

    def get_freq_of_keywords(self, keyword_list):
        word_list = self.headline.lower().split(" ") + self.text.lower().split(" ")
        freq = 0
        for word in word_list:
            if word in keyword_list:
                freq += 1
        return freq

    def __str__(self):
        ret_str = "Date: {} \tHeadline: {}{}".format(self.day.get_date_to_str(), self.headline[:20], "...") + "\t"
        ret_str += "Text: {}{}".format(self.text[:40], "...")
        return ret_str
