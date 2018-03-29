#!/usr/bin/env python
# -*- coding:utf-8 -*-
import glob
import numpy as np
import re


def file_feature(diric):
    all_feature=[]

    file = glob.glob(diric+"/feature_vector/*")
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)
    #print file
    #i=0

    for f in file:
        feat=np.loadtxt(f)
        feat=feat[:,1]
        all_feature.append(feat)
        #print f
    return all_feature


def sampling_read(diric):
    all_position=[] 
    file = glob.glob(diric+"/sampling_data/*")
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)
    for f in file:
        data=glob.glob(f+"/*")
        data.sort(key=alphanum_key)
        position=[]
        for d in data:

            p=np.loadtxt(d,delimiter=",")
            position.append(p)
            ##print d
        all_position.append(position)
    return all_position



def mu_read(diric):
    all_mu=[] 

    file = glob.glob(diric+'/mu/*')
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)
    #print file
    for f in file:
        mu=np.loadtxt(f)
        #print mu
        all_mu.append(mu)
    return all_mu


def sigma_read(diric):


    all_sigma=[] 
    
    file = glob.glob(diric+"/sigma/*.csv")
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)
    
    for f in file:
        sigma=np.loadtxt(f)
        all_sigma.append(sigma)
        
    return all_sigma


def phi_read(diric):
    all_fi=[] 
    file = glob.glob(diric+'/image_multi/*')
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)
    #print file
    for f in file:
        fi=np.loadtxt(f)
    
        return fi
def ramda_read(diric):
    all_ramda=[]
    file = glob.glob(diric+'/word/*')
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)

    for f in file:
        ramda=np.loadtxt(f,dtype=(str,str),delimiter=":")
        #fi=fi[:,1]
        ramda=map(float,ramda)
        all_ramda.append(ramda)
    return all_ramda


def position_data_read(diric):
    all_position=[] 

    file = glob.glob(diric+"/position_data/*")
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)
 
    for f in file:
        position=[] #(x,y,sin,cos)
        for line in open(f, 'r').readlines():
            data=line[:-1].split(' ')
            position +=[float(data[0])]
            position +=[float(data[1])]
        all_position.append(position)
    
    return all_position


def feature_data_read(diric):
    all_feature=[]

    file = glob.glob(diric+"/feature_vector/*")
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)

    for f in file:
        feat=np.loadtxt(f)
        try:
            feat=feat[:,1]
        except IndexError:
            pass
        all_feature.append(feat)
        #print f
    return all_feature


def cnn_feature_data_read(diric,S):
    all_feature=[]
    file = glob.glob(diric+"/feature4096/*")
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)
    for f in file:
        feat=np.loadtxt(f)
        feat=feat*S
        feat=feat.astype(np.int64)
        
        all_feature.append(feat)
    return all_feature

def word_data_read(diric,DATA_NUM,space_name,DATA_initial_index,word_class,W):
    file = glob.glob(diric+"/word/*")
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    file.sort(key=alphanum_key)

    all_word=[]
    word_data_ind=[]
    for i in range(DATA_NUM):
        word=[0 for n in range(word_class)]
        signal=(diric+"/word/word"+repr(i+DATA_initial_index)+".txt") in file
        
        if signal==True:
            word_data_ind.append(i)
            f=open(diric+"/word/word"+repr(i+DATA_initial_index)+".txt","r")
            data=f.read()
            line=data.split("\n")

            for j in range(word_class):
                for k in range(len(line)): 
                    if space_name[j]==line[k]:
                        word[j] +=W
                        #print word
                    else: 
                        pass
                        
        all_word.append(word)
    return all_word,word_data_ind