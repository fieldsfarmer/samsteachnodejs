import sys
import os
import codecs
import random

def get_twitters(input_file):
	twitters = []
	with open(input_file, 'r') as f_in:
		for line in f_in:
			line = line.decode('utf-8', 'ignore')
			twitters.append(line)

	return twitters

def write_twitters(twitters, output_file):
	with codecs.open(output_file, 'w', encoding='utf-8') as f_out:
		for twitter in twitters:
			f_out.write(twitter)

def sample_twitter(twitters, size):
	return random.sample(twitters, size)

if __name__ == '__main__':

	input_dir = sys.argv[1]
	output_dir = sys.argv[2]
	doc_min_size = int(sys.argv[3])
	doc_max_size = int(sys.argv[4])

	for fn in os.listdir(input_dir):
		fp = input_dir + '/' + fn
		twitters = get_twitters(fp)

		if len(twitters) < doc_min_size:
			continue

		if len(twitters) > 300:
			twitters = sample_twitter(twitters, doc_max_size)

		fp = output_dir + '/' + fn

		write_twitters(twitters, fp)
