import pickle
import os
from data_construct import *
import numpy
from sklearn import linear_model
import matplotlib.pyplot as plt

gt={}

ground_truth_file = open('./data/evaluation_data/labeled_data.txt')

for line in ground_truth_file:
    label = int(line.strip().split(':')[0]) 
    topic_id = line.strip().split(':')[1]
    gt[topic_id] = label

predict_dictionary = pickle.load(open('./data/model/eva_data'))
train = numpy.loadtxt('./data/model/training', delimiter='\t')
model = linear_model.LogisticRegression(penalty = 'l2')
model.fit(train[:,1:], train[:,0])

# print model.classes_
# all_count = 0.0
# true_count = 0.0
# for k, v in gt.iteritems():
#     all_count+=1
#     # print k, v
#     to_predict = predict_dictionary[k][1]
#     # print to_predict
#     predicted = model.predict_proba(to_predict)

#     # print predicted[0][0]
#     result = 1 if predicted[0][1]>0.5 else -1
#     if result == gt[k]:
#         # print predict_dictionary[k][0],"correct"
#         true_count+=1
    #     print "correct!!"
    #     print predict_dictionary[k][0]
    #     print "our prediction", result
    #     print 
    # else:
    #     print "wrong!!"
    #     print predict_dictionary[k][0]
    #     print predicted
    #     print "our prediction", result
    #     print 
# print "true count", true_count


# draw curve

precision = {}
recall = {}

test_thresholds= [ i/20.0 for i in range(0,20,1)]

# test_thresholds = [0.4]
print test_thresholds

for threshold in test_thresholds:
    true_pos=0.0
    predict_trues = 0.0
    gt_trues = 0.0

    for k,v in gt.iteritems():
        to_predict = predict_dictionary[k][1]
        predicted = model.predict_proba(to_predict)
        result = 1 if predicted[0][1]>threshold else -1
        gt_result = gt[k]
        if result==1 and gt_result==1:
            true_pos+=1
        if gt_result ==1:
            gt_trues+=1
        if result==1:
            predict_trues+=1

        if result==1 and gt_result==-1:
            print k, predict_dictionary[k][0]



    print "now theshold is ", threshold, "result is ",true_pos, gt_trues, predict_trues
    precision[threshold] = 1 if predict_trues==0 else true_pos/predict_trues
    recall[threshold] = true_pos/gt_trues

print precision
print recall

# plt.clf()
# plt.xlabel('Recall')
# plt.ylabel('Precision')
# plt.ylim([0.0, 1.05])
# plt.xlim([0.0, 1.0])

# X = [ recall[threshold] for threshold in test_thresholds]
# Y = [ precision[threshold] for threshold in test_thresholds]

# plt.plot(X,Y)
# plt.show()

# predict result

# for k,v in gt.iteritems():
#     to_predict = predict_dictionary[k][1]
#     predicted = model.predict_proba(to_predict)
#     score = model.decision_function(to_predict)
#     print k, predicted[0][1], score[0]



