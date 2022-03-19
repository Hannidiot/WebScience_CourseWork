from nltk import word_tokenize, pos_tag
from functools import reduce
from collections import Counter, defaultdict

import re
import numpy as np
import gensim

# from nltk.corpus import stopwords
# stop_words = stopwords.words('english')
# stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'not', 'would', 'say', 'could', '_', 'be', 'know', 'good', 'go', 'get', 'do', 'done', 'try', 'many', 'some', 'nice', 'thank', 'think', 'see', 'rather', 'easy', 'easily', 'lot', 'lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right', 'line', 'even', 'also', 'may', 'take', 'come'])


class TweetNewsWorthinessMarker:
    list_term = [
        "bus", "transport", "buses", "railway", "tram", "trams", "underground",
        "jam", "congestion", "accident", "accidents", "tfl", "traffic", "car",
        "cars", "pedestrian", "emergency"
    ]

    list_spam = [
        "ebay", "bitcoin", "bitcoins", "btc", "wallet", "money", "advertisement"
        'review', 'shopping', 'deal','sale', 'sales','link', 'click', 
        'marketing', 'promote', 'discount', 'products', 'store', 'diet', 'weight', 
        'porn', 'followback', 'lucky', 'winners', 'prize', 'hiring'
    ]

    def __init__(self, high_quality_set: list, low_quality_set: list):
        self.high_quality_set = high_quality_set
        self.low_quality_set = low_quality_set
        self.bg_set = high_quality_set + low_quality_set
        self.create_scoring_model()

    def generate_word_cnt(self, tweets):
        content_tweets = [tweet['text'] for tweet in tweets]
        data_words = list(self._process_tweets_to_words(content_tweets))
        word_list = reduce(lambda x, y: x + y, data_words)  # connect a two-dimension list to one-dimension
        ctr = Counter(word_list)

        return ctr, len(word_list)

    def create_scoring_model(self):
        self.bg_word_cnt, self.F_BG = self.generate_word_cnt(self.bg_set)
        self.hq_word_cnt, self.F_HQ = self.generate_word_cnt(self.high_quality_set)
        self.lq_word_cnt, self.F_LQ = self.generate_word_cnt(self.low_quality_set)

        self._calc_term_frequency()
        self._calc_term_score_table()

    def _process_tweets_to_words(self, tweets: list):
        for tweet in tweets:
            yield(self._tweet2words(tweet))

    def _tweet2words(self, tweet_content):
        # tweet_content = re.sub('\s+', ' ', tweet_content)  # remove newline chars
        # tweet_content = re.sub('http\S*', '', tweet_content)  # remove web url
        # tweet_content = re.sub("['\"“”’‘@]", '', tweet_content)    # remove symbol quotes
        # tweet_content = word_tokenize(str(tweet_content))
        # tweet_content = [item[0].lower() for item in filter(lambda item: item[1].startswith("N"), pos_tag(tweet_content))]  # only include noun words
        # tweet_content = [item.lower() for item in tweet_content if item.lower() not in stop_words]
        tweet_content = re.sub('\S*@\S*\s?', '', tweet_content)  # remove emails
        tweet_content = re.sub('\s+', ' ', tweet_content)  # remove newline chars
        tweet_content = re.sub("\'", "", tweet_content)  # remove single quotes
        words = gensim.utils.simple_preprocess(str(tweet_content), deacc=True) 
        return words

    def _calc_term_frequency(self):
        """
            calculate term frequency for specific terms and raw frequency of all terms
            for both HQ and LQ data
        """
        self.f_bg = defaultdict(lambda: 0)

        # create raw frequency of all terms and term frequency for HQ data
        self.f_hq = defaultdict(lambda: 0)
        for term in self.list_term:
            if term in self.hq_word_cnt.keys():
                self.F_HQ += self.hq_word_cnt[term]
                self.f_hq[term] += self.hq_word_cnt[term]
                self.f_bg[term] += self.bg_word_cnt[term]

        # create raw frequency of all terms and term frequency for LQ data
        self.f_lq = defaultdict(lambda: 0)
        for term in self.list_spam:
            if term in self.lq_word_cnt.keys():
                self.F_LQ += self.lq_word_cnt[term]
                self.f_lq[term] += self.lq_word_cnt[term]
                self.f_bg[term] += self.bg_word_cnt[term]

    def _calc_term_score_table(self):
        self.S_HQ = defaultdict(lambda: 0)
        self.S_LQ = defaultdict(lambda: 0)
        for term in self.f_hq.keys():
            R_HQ = (self.f_hq[term] / self.F_HQ) / (self.f_bg[term] / self.F_BG)
            if R_HQ >= 2.0:
                self.S_HQ[term] = R_HQ
        
        for term in self.f_lq.keys():
            R_LQ = (self.f_lq[term] / self.F_LQ) / (self.f_bg[term] / self.F_BG)
            if R_LQ >= 1.8:
                self.S_LQ[term] = R_LQ

    def mark(self, tweet):
        words = self._tweet2words(tweet)
        term_score = 1
        spam_score = 1
        for word in words:
            if word in self.S_HQ.keys():
                term_score += self.S_HQ[word]
        
        for word in words:
            if word in self.S_LQ.keys():
                spam_score += self.S_LQ[word]
        
        return np.log2(term_score/spam_score)

    def is_high_quality(self, tweet):
        return self.mark(tweet) > 0
    

if __name__ == '__main__':
    import json

    with open('/Users/minhao/Workspace/WS-Proj/CourseWork-M/data/highFileFeb', 'r') as f:
        high_value_set = []
        for line in f.readlines():
            high_value_set.append(json.loads(line))

    with open('/Users/minhao/Workspace/WS-Proj/CourseWork-M/data/lowFileFeb', 'r') as f:
        low_value_set = []
        for line in f.readlines():
            low_value_set.append(json.loads(line))
    
    t = TweetNewsWorthinessMarker(high_value_set, low_value_set)
    print(t.S_HQ)
    print(t.S_LQ)
