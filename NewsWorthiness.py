import re


from gensim.utils import simple_preprocess
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from functools import reduce
from collections import Counter


class TweetNewsWorthiness:

    def __init__(self, high_quality_set, low_quality_set):
        self.high_quality_set = high_quality_set
        self.low_quality_set = low_quality_set
        self.create_scoring_model()

    def generate_word_cnt(self, tweets, most_common=20):
        tweets_content = [tweet['text'] for tweet in tweets]
        data_words = list(self._process_words(tweets_content))
        data_no_stopwords = reduce(lambda x, y: x + y, data_words)
        ctr = Counter(data_no_stopwords)

        return ctr

    def create_scoring_model(self):
        # create high quality word list
        self.hq_word_cnt = self.generate_word_cnt(self.high_quality_set)
        self.list_term = self.hq_word_cnt.most_common(15)

        # create spam word list
        self.lq_word_cnt = self.generate_word_cnt(self.low_quality_set)
        self.list_spam = self.lq_word_cnt.most_common(15)

    def _process_words(self, tweets_content):
        for sent in tweets_content:
            sent = re.sub('\s+', ' ', sent)  # remove newline chars
            sent = re.sub('http\S*', '', sent)  # remove web url
            sent = re.sub("['\"“”’‘@]", '', sent)    # remove single quote
            sent = word_tokenize(str(sent))
            sent = [item[0].lower() for item in filter(lambda item: item[1].startswith("N"), pos_tag(sent))]
            yield(sent)

    def mark(self, tweet_content):
        pass

    def is_high_quality(self, tweet_content):
        pass
    

if __name__ == '__main__':
    import json

    with open('data/highFileFeb', 'r') as f:
        high_value_set = []
        for line in f.readlines():
            high_value_set.append(json.loads(line))

    with open('data/lowFileFeb', 'r') as f:
        low_value_set = []
        for line in f.readlines():
            low_value_set.append(json.loads(line))
    
    t = TweetNewsWorthiness(high_value_set, low_value_set)
    print(t.list_term)
    print(t.list_spam)
