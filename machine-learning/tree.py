# encoding: utf-8

import operator
from math import log


def create_dataset():
    dataset = [
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 2, 'maybe'],
        [3, 2, 'frid'],
        [4, 0, 'n1o'],
        [2, 3, 'no'],
    ]
    labels = ['no surfacing', 'flippers']
    return (dataset, labels)


def split_dataset(dataset, axis, value):
    """
    根据特征码 value
    分离数据，分类数据？
    """
    r = [f[:axis] + f[axis+1:]
         for f in dataset
         if f[axis] == value
        ]
    return r


def calc_shannon_entropy(dataset):
    num_entries = len(dataset)
    label_counts = {}
    for feat_vec in dataset:
        current_label = feat_vec[-1]
        if current_label not in label_counts:
            label_counts[current_label] = 0
        label_counts[current_label] += 1
    shannon_entropy = 0.0
    for key, value in label_counts.iteritems():
        prob = float(value)/num_entries
        shannon_entropy -= prob * log(prob, 2) # 以2为底求对数
    return shannon_entropy


def choose_best_feature_to_split(dataset):
    """
    选择最好的数据划分方式
    """
    num_features = len(dataset[0]) - 1
    base_entropy = calc_shannon_entropy(dataset)
    best_info_gain = 0.0 # 信息增量
    best_feature = -1
    dataset_size = len(dataset)

    for i in range(num_features):
        feat_list = [s[i] for s in dataset]
        unique_vals = set(feat_list)
        new_entropy = 0.0

        for value in unique_vals:
            sub_dataset = split_dataset(dataset, i, value)
            prob = len(sub_dataset)/float(dataset_size)
            new_entropy += prob * calc_shannon_entropy(sub_dataset)
        print('base_entropy', base_entropy, 'new_entropy', new_entropy)
        info_gain = base_entropy - new_entropy
        if (info_gain > best_info_gain):
            best_info_gain = info_gain
            best_feature = i
    return best_feature


def majority_cnt(class_list):
    class_count = {}
    for vote in class_list:
        if vote not in class_count:
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.iteritems(),
                                key=operator.itemgetter(1),
                                reverse=True)
    return sorted_class_count[0][0]


my_data, labels = create_dataset()
# print(calc_shannon_entropy(my_data))
feature = choose_best_feature_to_split(my_data)
print(feature)
# print(split_dataset(my_data, feature, 1))
