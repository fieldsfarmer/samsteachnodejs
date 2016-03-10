from data_construct import *

def feature_str_gen(cur):
    feature_str = ""
    try:
        noun_percentage, verb_percentage, adj_percentage, r_percentage = get_POS_percentage(cur.pos_tag_list)
        token_level_polarity_score = get_token_level_polarity_score(cur.sentiscore_list)
        pos_percentage, neg_percentage = get_tweet_level_senti_score(cur.sentiscore_list)
    except:
        return None
    feature_str+=str(noun_percentage)+'\t'+str(verb_percentage)+'\t'+str(adj_percentage)+'\t'+str(r_percentage)
    feature_str+='\t'+str(token_level_polarity_score)
    feature_str+='\t'+str(pos_percentage)+'\t'+str(neg_percentage)
    return feature_str


if __name__ == '__main__':

    output_dir = './data/model/'
    if sys.argv[1] == 'train':
        is_train = True
    else:
        is_train = False

    if is_train:
        data_handler = open(output_dir+'/pickled_training','w')
    else:
        data_handler = open(output_dir+'/pickled_test','w')

    start = time.time()

    pos_snapshot_file = open("./data/pos/pos_snapshots","r")
    neg_snapshot_file = open("./data/neg/neg_snapshots","r")

    pos_snapshots = pickle.load(pos_snapshot_file)
    neg_snapshots = pickle.load(neg_snapshot_file)


    for each in pos_snapshots:
        if is_train:
            data_handler.write('1')
        data_handler.write('\t')
        data_handler.write(feature_str_gen(each))
        data_handler.write('\n')
        data_handler.flush()

    for each in neg_snapshots:
        if is_train:
            data_handler.write('-1')
        data_handler.write('\t')
        data_handler.write(feature_str_gen(each))
        data_handler.write('\n')
        data_handler.flush()

    end = time.time()
    print "time cost : ", (end - start)


# print len(pos_snapshots)
# print len(neg_snapshots)