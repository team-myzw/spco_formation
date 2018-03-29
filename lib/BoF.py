#!/usr/bin/env python

import numpy as np

def bag_of_feature(feat,dim):

    count=np.zeros(dim)
    for z in feat:
        y_1 =np.array(z)
        count=count+y_1
    return count


def bag_of_words(feat,word_class):
    
    count=np.zeros(word_class)
    for z in feat:
        y_1 =np.array(z)
        count=count+y_1
    return count
