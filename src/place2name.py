# -*- coding:utf-8 -*-

import glob
import sys
import numpy as np
import re
from scipy.stats import multivariate_normal

TRAINING_PATH = "../training_data/"
RESULT_PATH = "../result/"

trial_name = sys.argv[1]

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

f = open(TRAINING_PATH + trial_name + "/space_name.txt")
hoge = f.read()
f.close()
place_name = hoge.split('\n')

cordinate=[float(sys.argv[2]),float(sys.argv[3]),0,0]
r_prob=np.ones(len(mu))
for x in xrange(-10,10):
    cordinate[2] = x * 0.1
    for y in xrange(-10,10):
        cordinate[3] = y * 0.1
        for z in xrange(len(mu)):
            r_prob[z] = multivariate_normal.pdf(cordinate, mean=mu[z], cov=sigma[z])
            r_prob[z] = r_prob[z] * pi[z]

word_prob = np.zeros(len(w[0]))
for x in xrange(len(mu)):
    for y in xrange(len(w[0])):
        for z in xrange(len(w[0])):
            word_prob[z] += w[y][z] * pi[x] * r_prob[x]
print word_prob

print place_name[np.argmax(word_prob)]

