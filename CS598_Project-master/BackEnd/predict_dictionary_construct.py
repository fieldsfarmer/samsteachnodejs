import pickle
import os
from data_construct import *
import numpy

model = pickle.load(open('./data/model/model_v1'))
to_predict_dir = "./data/predict_events/"
to_predict_model = "./data/model/to_predict/"

test_dic = {}
for snapshot_file in os.listdir(to_predict_dir):
    topic_id = snapshot_file.split('_')[0]
    # print topic_id
    cur = snapshots(to_predict_dir + snapshot_file)
    print "now dealing with topic id", topic_id
    try:
        noun_percentage, verb_percentage, adj_percentage, r_percentage = get_POS_percentage(
            cur.pos_tag_list)
        pos_percentage, neg_percentage = get_tweet_level_senti_score(
            cur.sentiscore_list)
        has_hashtag_percentage = get_has_hashtag_percentage(cur.hashtag_list)
        hashtag_per_tweet = get_hashtag_per_tweet(cur.hashtag_list)
        percentage_of_retweets = get_percentage_of_retweets(cur.tweets_list)
        token_level_polarity_score = get_token_level_polarity_score(
            cur.sentiscore_list)
        token_level_entropy = get_token_level_entropy(cur.sentiscore_list)
    except:
        print "error, file name is", snapshot_file

    to_predict_str = str(noun_percentage) + '\t' + str(verb_percentage) + '\t' + str(adj_percentage) + '\t' + str(r_percentage) + '\t' + str(pos_percentage) + '\t' + str(neg_percentage) + \
        '\t' + str(has_hashtag_percentage) + '\t' + str(hashtag_per_tweet) + '\t' + \
        str(percentage_of_retweets) + '\t' + \
        str(token_level_polarity_score) + '\t' + str(token_level_entropy)
    # test_dic[topic_id] = (snapshot_file, to_predict_str)
    to_write = open(to_predict_model+topic_id,"w")
    to_write.write(to_predict_str)
    to_write.close()
    to_read = open(to_predict_model+topic_id)
    test_dic[topic_id]= (snapshot_file, numpy.loadtxt(to_read, delimiter='\t'), cur)

pickle.dump(test_dic, open('./data/model/eva_data','w'))


