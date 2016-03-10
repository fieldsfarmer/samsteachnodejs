import sys
import os


def get_required_field_list(input):

	field_list = []
	with open(input, 'r') as f_in:
		for line in f_in:
			arr = line.strip().split(':')
			if len(arr) > 1:
				field_list.append(int(arr[1]))

	return field_list


def process_file(input, topic, output_dir, field_list):
	# topic_dir = output_dir + '/' + topic
	file_dict = {}

	with open(input, 'r') as f_in:
		for line in f_in:
			arr = line.split('\t')

			if len(arr) < 27:
				continue

			date = arr[0].replace('/', '-')

			if date not in file_dict:
				file_path = output_dir + '/'+topic+"#"+ date
				file_dict[date] = open(file_path, 'w')

			file_handler = file_dict[date]
			w_list = [arr[i] for i in field_list]
			w_line = '\t'.join(w_list) + '\n'
			file_handler.write(w_line)

	for date in file_dict:
		file_dict[date].close()

def process_file_newstweet(input, topic, output_dir, field_list):

	file_handler = open(output_dir+'/'+topic,"w")
	with open(input, 'r') as f_in:
		for line in f_in:
			arr = line.split('\t')

			if len(arr) < 27:
				continue

			date = arr[0].replace('/', '-')


			w_list = [arr[i] for i in field_list]
			w_line = '\t'.join(w_list) + '\n'
			file_handler.write(w_line)


	file_handler.close()

def batch_main_process(input):
	twitter_dir = input
	config_file = 'config_sample'
	output_dir = './data/predict_events/'
	os.mkdir(output_dir)
	feature_list = get_required_field_list(config_file)

	for topic_file in os.listdir(twitter_dir):

		print topic_file

		file_full_path = twitter_dir + '/' + topic_file

		process_file_newstweet(file_full_path, topic_file, output_dir, feature_list)


if __name__ == '__main__':

	twitter_dir = sys.argv[1]
	config_file = 'config_sample'
	output_dir = './events'

	feature_list = get_required_field_list(config_file)

	for topic_file in os.listdir(twitter_dir):

		print topic_file

		file_full_path = twitter_dir + '/' + topic_file
		process_file(file_full_path, topic_file, output_dir, feature_list)

