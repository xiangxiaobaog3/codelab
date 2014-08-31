# encoding: utf-8

import os

import numpy

from kNN import classify0

digits_dir_0 = 'digits/trainingDigits'
digits_dir_1 = 'digits/testDigits'

def img2vector(filename):
    v = numpy.zeros((1, 1024))

    with open(filename) as fb:
        for i in range(32):
            line = fb.next()
            for j in range(32):
                v[0,32*i+j] = int(line[j])
    return v


def get_class_num_from_filename(filename):
    filestr = filename.split('.')[0]
    class_num = int(filestr.split('_')[0])
    return class_num


def handwriting_test_class():
    hw_labels = []
    training_filter_list = os.listdir(digits_dir_0)
    m = len(training_filter_list)
    training_mat = numpy.zeros((m, 1024)) # 空间存储

    for i in range(m):
        filename = training_filter_list[i]
        class_num = get_class_num_from_filename(filename)
        hw_labels.append(class_num)
        training_mat[i, :] = img2vector(os.path.join(digits_dir_0, filename))
    test_file_list = os.listdir(digits_dir_1)
    error_count = 0.0

    m_test = len(test_file_list)

    for i in range(m_test):
        filename = test_file_list[i]
        class_num = get_class_num_from_filename(filename)
        vector_under_test = img2vector(os.path.join(digits_dir_1, filename))
        classifier_result = classify0(vector_under_test,
                                      training_mat,
                                      hw_labels,
                                      3)
        print("the classifier came back with: %d, the real answer is: %d" % classifier_result, class_num)
        if classifier_result != class_num:
            error_count += 1.0
    print("\nthe total number of errors is: %d" % error_count)
    print("\nthe total error rate of is: %f" % (error_count/float(m_test)))

handwriting_test_class()

print(img2vector(os.path.join(digits_dir_0, '1_1.txt')))
