import re


from nltk import word_tokenize, pos_tag
from functools import reduce
from collections import Counter
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'not', 'would', 'say', 'could', '_', 'be', 'know', 'good', 'go', 'get', 'do', 'done', 'try', 'many', 'some', 'nice', 'thank', 'think', 'see', 'rather', 'easy', 'easily', 'lot', 'lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right', 'line', 'even', 'also', 'may', 'take', 'come'])


class TweetNewsWorthiness:

    def __init__(self, high_quality_set, low_quality_set, most_common=20):
        self.high_quality_set = high_quality_set
        self.low_quality_set = low_quality_set
        self._most_common = most_common
        self.create_scoring_model()

    def generate_word_cnt(self, tweets):
        tweets_content = [tweet['text'] for tweet in tweets]
        data_words = list(self._process_models(tweets_content))
        data_no_stopwords = reduce(lambda x, y: x + y, data_words)
        ctr = Counter(data_no_stopwords)

        return ctr

    def create_scoring_model(self):
        # create high quality word list
        self.hq_word_cnt = self.generate_word_cnt(self.high_quality_set)
        self.list_term = self.hq_word_cnt.most_common(self._most_common)

        # create spam word list
        self.lq_word_cnt = self.generate_word_cnt(self.low_quality_set)
        self.list_spam = self.lq_word_cnt.most_common(self._most_common)

    def _process_models(self, tweets: list):
        for tweet in tweets:
            yield(self._tweet2words(tweet))

    def _tweet2words(self, tweet_content):
        tweet_content = re.sub('\s+', ' ', tweet_content)  # remove newline chars
        tweet_content = re.sub('http\S*', '', tweet_content)  # remove web url
        tweet_content = re.sub("['\"“”’‘@]", '', tweet_content)    # remove symbol quotes
        tweet_content = re.sub("^\w\s", '', tweet_content)
        tweet_content = word_tokenize(str(tweet_content))
        tweet_content = [item[0].lower() for item in filter(lambda item: item[1].startswith("N"), pos_tag(tweet_content))]  # only include noun words
        # tweet_content = [item.lower() for item in tweet_content if item.lower() not in stop_words]
        return tweet_content

    def mark(self, tweet):
        pass

    def is_high_quality(self, tweet):
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
