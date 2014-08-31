#!/usr/bin/env python
# encoding: utf-8


import operator

import matplotlib
import matplotlib.pyplot as plt
from numpy import array, tile, zeros, shape

def create_data_set():
    group = array([
        [1.0, 1.1],
        [1.0, 1.0],
        [0.0, 0.0],
        [0.0, 0.1],
    ])
    labels = ['A', 'A', 'B', 'B']
    return (group, labels)


def classify0(in_x, data_set, labels, k):
    data_set_size = data_set.shape[0] # row number
    # 距离计算
    diffmt = tile(in_x, (data_set_size, 1)) - data_set
    sq_diff_mat = diffmt ** 2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances ** 0.5
    sorted_dist_indices = distances.argsort()

    class_count = {}
    for i in range(k):
        vote_ilabel = labels[sorted_dist_indices[i]]
        class_count[vote_ilabel] = class_count.get(vote_ilabel, 0) + 1
    sorted_class_count = sorted(class_count.iteritems(),
                                key=operator.itemgetter(1),
                                reverse=True)
    return sorted_class_count[0][0]

def file2matrix(filename):
    with open(filename) as fb:
        lines = fb.readlines()
        number_of_lines = len(lines)
        return_mat = zeros((number_of_lines, 3))
        class_label_vector = []
        index = 0

        for line in lines:
            line = line.strip()
            list_from_line = line.split('\t')
            return_mat[index,:] = list_from_line[0:3]
            class_label_vector.append(int(list_from_line[-1]))
            index += 1

        return return_mat, class_label_vector


def auto_norm(dataset):
    """归一化数值:
    公式 newVal = (oldVal-min)/(max-min)
    """
    min_vals = dataset.min(0)
    max_vals = dataset.max(0)
    ranges = max_vals - min_vals
    norm_dataset = zeros(shape(dataset)) # verbose step
    m = dataset.shape[0]
    norm_dataset = dataset - tile(min_vals, (m, 1))
    norm_dataset = norm_dataset / tile(ranges, (m, 1))
    return (norm_dataset, ranges, min_vals)


def dating_class_test():
    ho_ratio = 0.10
    dating_dataset, dating_labels = file2matrix('datingTestSet2.txt')
    norm_mat, ranges, min_vals = auto_norm(dating_dataset)
    m = norm_mat.shape[0] # lines
    num_test_vecs = int(m*ho_ratio)
    error_count = 0.0

    for i in range(num_test_vecs):
        classifier_result = classify0(norm_mat[i,:],
                                      norm_mat[num_test_vecs:m,:],
                                      dating_labels[num_test_vecs:m],
                                      3)
        print("the classifier came back with: %d, the real answer is: %d" %
              (classifier_result, dating_labels[i]))
        if (classifier_result != dating_labels[i]):
            error_count += 1.0
    print("the total error rate is: %f" % (error_count/float(num_test_vecs)))

# dating_class_test()

def classify_person():
    result_list = ['not at all', 'in small doses', 'in large doses']
    percent_tats = float(raw_input("percentage of time spent playing video game?"))
    ff_miles = float(raw_input("frequent flier miles earned per year?"))
    ice_cream = float(raw_input("liters of ice cream consumed per year?"))
    dating_dataset, dating_labels = file2matrix('datingTestSet2.txt')
    norm_mat, ranges, min_vals = auto_norm(dating_dataset)
    in_arry = array([ff_miles, percent_tats, ice_cream])
    classifier_result = classify0((in_arry-min_vals)/ranges,
                                  norm_mat,
                                  dating_labels,
                                  3)
    print("you will probably like this person: ", result_list[classifier_result - 1])


# classify_person()

# group, labels = create_data_set()
# print(classify0([1001010, 10, 100], group, labels, 3))
dating_data_matrix, dating_data_labels = file2matrix('datingTestSet2.txt')
dating_data_matrix, ranges, min_vals = auto_norm(dating_data_matrix)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dating_data_matrix[:,1], dating_data_matrix[:,2],
           15.0 * array(dating_data_labels), 15.0 * array(dating_data_labels))
# plt.show()
