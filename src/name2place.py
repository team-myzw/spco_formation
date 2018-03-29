# -*- coding:utf-8 -*-

import glob
import sys
import numpy as np
import re
from scipy.stats import multivariate_normal

TRAINING_PATH = "../training_data/"
RESULT_PATH = "../result/"

trial_name = sys.argv[1]
target_place = sys.argv[2]

mu = []
file = glob.glob(RESULT_PATH + trial_name + '/mu/*')
convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
file.sort(key = alphanum_key)
for f in file:
    hoge = np.loadtxt(f)
    mu.append(hoge)

sigma = []
file = glob.glob(RESULT_PATH + trial_name + "/sigma/*.csv")
file.sort(key = alphanum_key)
for f in file:
    hoge = np.loadtxt(f)
    sigma.append(hoge)

w = []
file = glob.glob(RESULT_PATH + trial_name + '/word/*')
file.sort(key = alphanum_key)
for f in file:
    hoge = np.loadtxt(f,dtype = (str,str),delimiter = ":")
    hoge = map(float,hoge)
    w.append(hoge)

pi = np.loadtxt(RESULT_PATH + trial_name + "/pi.csv")

f = open(TRAINING_PATH + "trial" + "/space_name.txt")
hoge = f.read()
f.close()
place_name = hoge.split('\n')

word_class = -1
for x in xrange(len(place_name)):
    if place_name[x] == target_place:
        word_class = x
if word_class == -1:
    print "I don't know that place."

prob = np.array([0.0 for k in xrange(len(w))])
for x in xrange(len(mu)):
    prob[x] = w[x][word_class] * pi[x]

# print prob
print np.argmax(prob)
c = np.argmax(prob)

print mu[c]
#print sigma[c]

#print multivariate_normal.rvs(mean = mu[c], cov = sigma[c], size = 1)

