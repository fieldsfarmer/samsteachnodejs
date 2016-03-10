from sklearn import linear_model
import sys
import numpy
import pickle

def train_and_predict(train_file, test_file):

	train = numpy.loadtxt(train_file, delimiter='\t')
	test = numpy.loadtxt(test_file, delimiter='\t')

	model = linear_model.LogisticRegression(penalty = 'l2')
	model.fit(train[:,1:], train[:,0])

	return model.predict_proba(test)

if __name__ == '__main__':

	# train_file = sys.argv[1]
	# test_file = sys.argv[2]

	# for r in train_and_predict(train_file, test_file):
	# 	print r

    train = numpy.loadtxt('./data/model/training', delimiter='\t')
    model = linear_model.LogisticRegression(penalty = 'l2')
    model.fit(train[:,1:], train[:,0])
    pickle.dump(model, open('./data/model/modelv_1','w'))
