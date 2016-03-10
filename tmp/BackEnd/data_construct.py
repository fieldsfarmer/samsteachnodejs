import sys
import os
import time
from feature_utilities import *
import pickle

def normalization(raw_text):
    # to implement normalizaion of tweet text including \xe elimination, RT elimination, http elimination
    # now only easiest way for normalization
    text = raw_text[3:] if raw_text[:3]=="RT " else raw_text
    text_fields = text.split()
    text = ' '.join([each for each in text_fields if "http" not in each])
    return text

def eliminate_unicode(token):
    try:
        i = token.lower().index('\u')
    except:
        i = -5
    if i!=-5:
        token=token[:i]
    return token

class snapshots:

    def __init__(self,snapshot_file_path):
        self.file_path = snapshot_file_path
        snapshot_file = open(snapshot_file_path,"r")
        self.tweets_list = []
        self.texts_list = []
        # token, nltk tag
        self.pos_tag_list=[]
        # token, wordnet tag
        self.wordnet_tag_list=[]
        self.sentiscore_list=[]
        # lemmetized token, wordnet tag
        self.ltoken_tag_list=[]
        self.topic =  " ".join(snapshot_file_path.split("/")[-1].split("#")[0].split("_"))
        self.hashtag_list = []
        for line in snapshot_file:
            # print line
            # line = line.decode('utf-8', 'ignore')
            line = line.decode('unicode_escape').encode('ascii','ignore')
            self.tweets_list.append(line[:-1])
            
            self.texts_list.append(normalization(line[:-1].split('\t')[1]))
            # print line
            hashtags = line[:-1].split('\t')[4].split(',')
            if hashtags==[""]:
                self.hashtag_list.append([])
            else:
                self.hashtag_list.append(hashtags)
        for sentence in self.texts_list:
            tokens = tokenizer.tokenize(sentence)
            # print tokens
            tokens_postag = nltk.pos_tag(tokens)
            # print tokens_postag
            self.pos_tag_list.append(tokens_postag)

            wordnet_tag = []
            for each_pair in tokens_postag:
                if 'NN' in each_pair[1]:
                    wordnet_tag.append( (each_pair[0],'n'))
                if 'JJ' in each_pair[1]:
                    wordnet_tag.append( (each_pair[0],'a'))
                elif 'RB' in each_pair[1]:
                    wordnet_tag.append( (each_pair[0],'r'))
                elif 'VB' in each_pair[1]:
                    wordnet_tag.append( (each_pair[0],'v'))
            self.wordnet_tag_list.append(wordnet_tag)

            # lemmatized tokens are lemmatized and lowered
            ltoken_tag = []
            for each_pair in wordnet_tag:
                lword = lemmatizer.lemmatize(each_pair[0],each_pair[1])
                ltoken_tag.append((lword.lower(), each_pair[1]))
            self.ltoken_tag_list.append(ltoken_tag)

            tweet_senti_score = []

            for each_pair in ltoken_tag:
                each_score = sentiextractor.get_score(each_pair)
                if abs(each_score)>0.02:
                    tweet_senti_score.append(each_score)
                else:
                    tweet_senti_score.append(0)
            self.sentiscore_list.append(tweet_senti_score)


if __name__ == '__main__':


    # test code
   

    # print test_snapshot.topic
    # print test_snapshot.tweets_list


    # start = time.time()

    # output_dir = './data/model/'

    # test_dir = './data/test/'

    # pos_snapshots = []
    # neg_snapshots = []
   
    # target_dir = [test_dir]

    # for cur_dir in target_dir:
    #     for snapshot_file in os.listdir(cur_dir):
    #         print "now dealing with file", snapshot_file
    #         cur = snapshots(cur_dir+snapshot_file)
    #         # print cur.texts_list
    #         # print get_token_level_entropy(cur.sentiscore_list)
    #         print get_hashtag_per_tweet(cur.hashtag_list)
    #         print get_has_hashtag_percentage(cur.hashtag_list)
    #         print get_percentage_of_retweets(cur.tweets_list)
    # model training code

    if sys.argv[1] == 'train':
        is_train = True
    else:
        is_train = False

    start = time.time()

    pos_dir = "./data/pos/sampled_events/"

    neg_dir = "./data/neg/sampled_events/"
    output_dir = './data/model/'

    test_dir = './data/test/'

    pos_snapshots = []
    neg_snapshots = []

    pos_snapshot_file = open("./data/pos/pos_snapshots","w")
    neg_snapshot_file = open("./data/neg/neg_snapshots","w")

    if is_train:
        data_handler = open(output_dir+'/training','w')
    else:
        data_handler = open(output_dir+'/test','w')

    if is_train:
        target_dir = [pos_dir, neg_dir]
    else:
        target_dir = [test_dir]

    for cur_dir in target_dir:
        for snapshot_file in os.listdir(cur_dir):
            print "now dealing with file", snapshot_file
            cur = snapshots(cur_dir+snapshot_file)
            if cur_dir == pos_dir:
                pos_snapshots.append(cur)
            else:
                neg_snapshots.append(cur)
            try:
                noun_percentage, verb_percentage, adj_percentage, r_percentage = get_POS_percentage(cur.pos_tag_list)
                pos_percentage, neg_percentage = get_tweet_level_senti_score(cur.sentiscore_list)
                has_hashtag_percentage = get_has_hashtag_percentage(cur.hashtag_list)
                hashtag_per_tweet = get_hashtag_per_tweet(cur.hashtag_list)
                percentage_of_retweets = get_percentage_of_retweets(cur.tweets_list)
                token_level_polarity_score = get_token_level_polarity_score(cur.sentiscore_list)
                token_level_entropy = get_token_level_entropy(cur.sentiscore_list)
            except:
                continue

            if is_train:
                if cur_dir == pos_dir:
                    data_handler.write('1')
                else:
                    data_handler.write('-1')

                data_handler.write('\t')
                
            data_handler.write(str(noun_percentage)+'\t'+str(verb_percentage)+'\t'+str(adj_percentage)+'\t'+str(r_percentage))
            data_handler.write('\t'+str(pos_percentage)+'\t'+str(neg_percentage))
            data_handler.write('\t'+str(has_hashtag_percentage)+'\t'+str(hashtag_per_tweet))
            data_handler.write('\t'+str(percentage_of_retweets))
            data_handler.write('\t'+str(token_level_polarity_score)+'\t'+str(token_level_entropy))
            data_handler.write('\n')
            data_handler.flush()
            # print cur.topic
            # print cur.tweets_list[0]
            # print cur.texts_list
            # print cur.pos_tag_list
            # print cur.wordnet_tag_list
            # print get_POS_percentage(cur.pos_tag_list)
            # print cur.sentiscore_list
            # print len(cur.sentiscore_list)
            # print len(cur.texts_list)
            # print get_token_level_polarity_score(cur.sentiscore_list)
            # for i in xrange(len(cur.sentiscore_list)):
            #     print cur.texts_list[i],
            #     tweet_score = 0
            #     for each_score in cur.sentiscore_list[i]:
            #         tweet_score+=each_score
            #     print tweet_score

    end = time.time()
    pickle.dump(pos_snapshots,pos_snapshot_file)
    pickle.dump(neg_snapshots,neg_snapshot_file)

    print "time cost : ", (end - start)

        

        