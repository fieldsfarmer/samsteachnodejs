import os
predict_dir = './data/predict_data/'

output_dir = './data/predict_data_withdate/'

os.mkdir(output_dir)

for topic_file in os.listdir(predict_dir):

        new_file = open(output_dir+topic_file,"w")

        for line in open(predict_dir+topic_file):
            # print line
            new_file.write('data\t'+line)
        new_file.close

