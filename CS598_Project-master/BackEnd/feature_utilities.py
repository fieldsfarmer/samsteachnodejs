import sys
import os
import pickle
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.tag import *
from nltk.corpus import treebank
import math
# from data_construct import snapshots

# noun, verb, adj, r_token
class MySentiWordExtractor:
    def __init__(self):
        f = open("./SentiWordNet_1.0.1.txt")
        self.term_sent = {}
        for line in f.readlines():
            if line[0]!='#':
                cols = line.split('\t')
                pos = cols[0]
                # print cols[2],"!",cols[3]
                score = float(cols[2]) -float(cols[3])
                words = cols[4].split(' ')
                for word_rank in words:
                    word = word_rank.split('#')[0]
                    rank = int(word_rank.split('#')[2])
                    synterm = word+"#"+pos
                    if synterm not in self.term_sent:
                        self.term_sent[synterm] = {}
                    self.term_sent[synterm][rank] = score
    def get_score(self, (word,pos)):
        query = word+'#'+pos
        if query not in self.term_sent:
            return 0
        else:
            score = 0.0;
            denominator = 0.0;
            for k, v in self.term_sent[query].iteritems():

                denominator+=1.0/k
                score+= v* 1.0/k
                # print k, denominator, score
            score = score / denominator
            return score

    def get_second_score(self, (word,pos)):
        poss = ['a','r','v','n']
        poss.remove(pos)
        candidates = []
        for each in poss:

            if self.get_score((word,each))!=0:
                return self.get_score((word,each))
        return 0
    def get_first_score(self,(word,pos)):
        query = word+'#'+pos
        if query not in self.term_sent:
            return 0
        else:
            score = 0.0;
            denominator = 0.0;
            for k, v in self.term_sent[query].iteritems():
                if k<3:
                    denominator+=1.0/k
                    score+= v* 1.0/k
                # print k, denominator, score
            score = score / denominator
            return score

tokenizer = TreebankWordTokenizer()
english_stops = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
sentiextractor = MySentiWordExtractor()

def get_POS_percentage(pos_tag_list):
    all_token_count = 0
    noun_token_count = 0
    verb_token_count = 0
    adj_token_count = 0
    r_token_count = 0
    for pos_tags in pos_tag_list:
        # print tokens_postag
        all_token_count+=len(pos_tags)
        for each_pair in pos_tags:
            if 'NN' in each_pair[1]:
                noun_token_count += 1
                # print each_pair[0]
            elif 'JJ' in each_pair[1]:
                adj_token_count += 1
            elif 'VB' in each_pair[1]:
                verb_token_count += 1
            elif 'RB' in each_pair[1]:
                r_token_count += 1
    return (float(noun_token_count)) / all_token_count, (float(verb_token_count)) / all_token_count, (float(adj_token_count)) / all_token_count, (float(r_token_count)) / all_token_count

def get_token_level_polarity_score(sentiscore_list):

    pos_token = 0.0
    neg_token = 0.0
    all_token = 0.0

    for each_tweet_list in sentiscore_list:
        for score in each_tweet_list:
            all_token+=1
            if score>0.6:
                pos_token+=2
            elif score<-0.6:
                neg_token+=2

            elif score<0 and score>=-0.6:
                neg_token+=1
            elif score>0 and score<=0.6:
                pos_token+=1
    # print pos_token, neg_token, all_token
    return (pos_token+neg_token)/all_token* ( min(pos_token, neg_token)/ max(pos_token,neg_token))


def get_token_level_entropy(sentiscore_list):
    senti_ranges = [0.0]*10
    for each_tweet_list in sentiscore_list:
        for score in each_tweet_list:
            if score<=-1:
                senti_ranges[0]+=1
            elif score>-1 and score<=-0.8:
                senti_ranges[1]+=1
            elif score>-0.8 and score<=-0.6:
                senti_ranges[2]+=1
            elif score>-0.6 and score<=-0.4:
                senti_ranges[3]+=1
            elif score>-0.4 and score<=-0.2:
                senti_ranges[4]+=1
            elif score >=0.2 and score <0.4:
                senti_ranges[5]+=1
            elif score >=0.4 and score <0.6:
                senti_ranges[6]+=1
            elif score >=0.6 and score <0.8:
                senti_ranges[7]+=1
            elif score >=0.8 and score <1:
                senti_ranges[8]+=1
            elif score>=1:
                senti_ranges[9]+=1
    all_token = sum(senti_ranges)
    senti_possibility_ranges = [i/all_token for i in senti_ranges]

    entropy = 0.0
    for each in senti_possibility_ranges:
        if each==0:
            continue
        else:
            entropy-= each * math.log(each,2)
    return entropy/ math.log(10,2)


def get_percentage_of_retweets(tweets_list):

    all_texts = 0.0
    retweet_texts = 0.0
    for text in tweets_list:
        all_texts+=1
        if "RT @" in text:
            retweet_texts+=1
            # print text
    return retweet_texts/ all_texts

def get_tweet_level_senti_score(sentiscore_list):
    pos_tweet = 0.0
    neg_tweet = 0.0
    all_tweet = 0.0
    for each_tweet_list in sentiscore_list:
        all_tweet+=1
        tweet_score = 0
        for each_score in each_tweet_list:
            tweet_score+=each_score
        if tweet_score>0.2:
            pos_tweet+=1
        if tweet_score<-0.2:
            neg_tweet+=1
    # print pos_token, neg_token, all_token
    return pos_tweet/all_tweet, neg_tweet/all_tweet

def get_hashtag_per_tweet(hashtag_list):
    all_tweet = 0.0
    hash_tag_count = 0.0
    for hashtags in hashtag_list:
        # print hashtags, len(hashtags)
        all_tweet+=1
        hash_tag_count+=len(hashtags)
    per_tweet =  hash_tag_count/all_tweet

    result = per_tweet
    if result>1:
        result = 1
    return result

def get_has_hashtag_percentage(hashtag_list):
    all_tweet = 0.0
    has_hashtag = 0.0
    for hashtags in hashtag_list:
        all_tweet+=1
        if len(hashtags)>0:

            has_hashtag+=1
    return has_hashtag/all_tweet


if __name__ == '__main__':
    print MySentiWordExtractor().term_sent
    # pass

