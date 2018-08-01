#!/usr/bin/env python
# -*- coding:utf-8 -*-
##########################################
#Gibbs sampling for training Place concept 
#Author Satoshi Ishibushi

#-==========================================-

##########################################
import argparse
import numpy as np
import random
import string
import sys
import glob
import re
import math
import os
from numpy.linalg import inv, cholesky
from scipy.stats import chi2
import time
sys.path.append("../lib/")
import BoF
import Prob_Cal
import Multi
import file_read as f_r
import nonpara_tool

def makedirs(path):
    try:
        os.makedirs(path)
    except:
        pass

CNN_feature=0 #If you want to use image feature of 4096 dimensions,you shold set 1.

parser = argparse.ArgumentParser()
parser.add_argument(
    "Training_directory",
    help="Input training directory."
)
parser.add_argument(
    "Output_directory",
    help="Output result directory."
)
parser.add_argument(
    "--slide",
    default=1,
    help="Sliding num for reading training data."
)
parser.add_argument(
    "--Nonpara",
    default=1,
    type=int,
    help="If you use nonparametric Bayse model, you should set True."
)
parser.add_argument(
    "--Word",
    default=1,
    type=int,
    help="If you use modality of word, you should set this value as True."
)
args = parser.parse_args()
data_diric=args.Training_directory
Out_put_dir="../result/"+args.Output_directory
Slide=int(args.slide)
#===================Environment_parameter=========================
env_para=np.genfromtxt(data_diric+"/Environment_parameter.txt",dtype= None,delimiter =" ")
#print env_para

MAP_X =env_para[0][1]  #Max x value of the map
MAP_Y =env_para[1][1]  #Max y value of the map
map_x =env_para[2][1] #Min x value of the map
map_y =env_para[3][1] #Max y value of the map
map_center_x = ((MAP_X - map_x)/2)+map_x
map_center_y = ((MAP_Y - map_x)/2)+map_y
clas_num=env_para[4][1]
DATA_initial_index= int(env_para[5][1]) #Initial data num
DATA_last_index= int(env_para[6][1]) #Last data num
DATA_NUM =DATA_last_index - DATA_initial_index +1
Learnig_data_num=(DATA_last_index - DATA_initial_index +1)/Slide #Data number

if args.Word==1:
    args.Word=True
else:
    args.Word=False

if args.Nonpara==1:
    args.Nonpara=True
else:
    args.Nonpara=False

if CNN_feature==0:
    FEATURE_DIM =1000# Image feature dimension
else:
    FEATURE_DIM =4096
Stick_large_L=100
sigma_init = 100.0 #initial covariance value
iteration = 50 #iteration num
#=========================Hyper parameter=====================
hyper_para=np.loadtxt("../parameter/gibbs_hyper_parameter.txt",delimiter=" #",skiprows=2)
alfa = hyper_para[0]
kappa_0=hyper_para[1]
nu_0=hyper_para[2]
mu_0=np.array([map_center_x,map_center_y,0.0,0.0])
psai_0=np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
gamma=hyper_para[3]
beta =hyper_para[4]
S=10 
W=20
if args.Word:
    space_name=[]
    for line in open(data_diric+"/space_name.txt","r"):
        line=line.rstrip()
        space_name.append(line)

    word_class=len(space_name)
else:
    word_class=0
start_time=time.time()
#<<<<<<<<<<<<<>Gibbs sampling>>>>>>>>>>>>>|||||||||||||||||||||||||||||||||||||||||||||>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def gibbs(data_pose,data_feature,data_word,word_data_ind):

    if args.Nonpara:

        pi=nonpara_tool.stick_breaking(gamma,Stick_large_L)
        clas_num=len(pi)
        print "Stick breakin process done．"
    else:
        global clas_num
    print clas_num
    #Initializing the mean of Gussian distribution 

    Myu_Ct =np.array([[random.uniform(map_x,MAP_X ),random.uniform(map_y,MAP_Y),random.uniform(-1,1),random.uniform(-1,1)] for i in xrange(clas_num)])
    #########======initialize Gaussian parameter:mu===========###########
    for j in range(clas_num):
        index=random.uniform(0,clas_num)
        p=data_pose[int(index)]
        Myu_Ct[0]=p
    #########==================#############
    initial_mu=[]
    for i,p in enumerate(Myu_Ct):
        initial_mu.append(p) 
    initial_mu=np.array(initial_mu)
    #Initializing covariance matrix of positional Gaussian dis
    Sigma_Ct =[np.matrix([[sigma_init,0.0,0.0,0.0],[0.0,sigma_init,0.0,0.0],[0.0,0.0,sigma_init,0.0],[0.0,0.0,0.0,sigma_init]]) for i in range(clas_num)]

    #Initializing the mean of Multinomial distribution for Image features
    fi_Ct = np.array([[float(1.0)/FEATURE_DIM for i in range(FEATURE_DIM)] for j in range(clas_num)])
    if args.Word:
    #Initializing the mean of Multinomial distribution for Words
        ramda_Ct=np.array([[float(1.0)/word_class for i in range(word_class)] for j in range(clas_num)])

    
    C_t = np.array([n for n in xrange(clas_num)])
    
    #Initializing class index of data.
    data_c= np.array([1000 for n in xrange(DATA_NUM)])




    for iter in xrange(iteration):
        print 'Iteration.'+repr(iter+1)+'\n'

        #<<<<<Sampling class index C_t<<<<
	  	 
        print 'Sampling calss index...\n'
	  	 
        for d in xrange(0,DATA_NUM,Slide):

            prob_C_t=np.array([0.0 for i in xrange(clas_num)]) 

            for i in range(clas_num):
                prob_C_t[i] += Prob_Cal.multi_gaussian_log(data_pose[d],Myu_Ct[i],Sigma_Ct[i])
                prob_C_t[i]+=math.log(pi[i])
                
                prob_C_t[i] +=Prob_Cal.multi_nomial_log(data_feature[d],fi_Ct[i])

                if args.Word:
                    if sum(data_word[d])!=0:
                        data_word[d]=np.array(data_word[d])
                        prob_C_t[i]+= Prob_Cal.multi_nomial_log(data_word[d],ramda_Ct[i])
                        
            max_class =np.argmax(prob_C_t)
            prob_C_t -=prob_C_t[max_class]
            prob_C_t =np.exp(prob_C_t)
            prob_C_t = Prob_Cal.normalize(prob_C_t)#Normalize weight.

            data_c[d] =np.random.choice(C_t,p=prob_C_t)
            print 'Iteration:',iter+1,'Data:',d+DATA_initial_index,'max_prob',max_class,":",prob_C_t[max_class],'Class index',data_c[d]
		 
        #<<<<<Sampling Gaussian parameter Myu_Ct , Sigma_Ct.
		 
        print 'Started sampling parameters of Position Gaussian dist...\n'

        for c in xrange(clas_num):
            pose_c=[]
            #========Calculating average====
            for d in xrange(len(data_c)):
                if data_c[d]==c:
                    pose_c.append(data_pose[d])
            sum_pose=np.array([0.0,0.0,0.0,0.0])
            for i in xrange(len(pose_c)):
                for j in xrange(4):
                    sum_pose[j] +=pose_c[i][j]
			
            bar_pose=np.array([0.0,0.0,0.0,0.0])
            for i in xrange(4):
                if sum_pose[i] !=0:		 	
                    bar_pose[i]=sum_pose[i]/len(pose_c)

			#=========Calculating Mu=============
            Mu = (kappa_0*mu_0+len(pose_c)*bar_pose)/(kappa_0+len(pose_c))

            #=========Calculating Matrix_C===================
            bar_pose_matrix=np.matrix(bar_pose)
				
            Matrix_C =np.zeros([4,4])
            for i in xrange(len(pose_c)):
                pose_c_matrix = np.matrix(pose_c[i])
                Matrix_C +=((pose_c_matrix- bar_pose_matrix).T*(pose_c_matrix- bar_pose_matrix))

            #=======Calculating Psai===============
            ans = ((bar_pose_matrix - mu_0).T * (bar_pose_matrix - mu_0))*((kappa_0*len(pose_c))/(kappa_0+len(pose_c)))
            Psai = psai_0 + Matrix_C + ans
		 	
		 	#=======Updating hyper parameter:Kappa,Nu===============================
            Kappa = kappa_0 + len(pose_c)
            Nu = nu_0 + len(pose_c)

		 	#============Sampling fron wishrt dist====================
		 
            Sigma_Ct[c]=Prob_Cal.sampling_invwishartrand(Nu,Psai)
            Sigma_temp=Sigma_Ct[c]/Kappa


            
            Myu_Ct[c]= np.random.multivariate_normal(Mu,Sigma_temp)
            
            #No asigned data
            if len(pose_c)==0:
                index=random.uniform(0,clas_num)
                p=data_pose[int(index)]
                Myu_Ct[c]=p
                #Myu_Ct[c]=[random.uniform(map_x,MAP_X ),random.uniform(map_y,MAP_Y),random.uniform(-1,1),random.uniform(-1,1)] 
                Sigma_Ct[c]=np.matrix([[sigma_init,0.0,0.0,0.0],[0.0,sigma_init,0.0,0.0],[0.0,0.0,sigma_init,0.0],[0.0,0.0,0.0,sigma_init]])
            #print Myu_Ct[c]
            #print Sigma_Ct[c]
	
		
        print 'Finished sampling parameters of Position Gaussian dist...\n'
		

        #<<<<<<Sampling Parameter of Multinomial fi_Ct>>>>>>>>>>>>>>>>>>
	  	 
        
        print 'Started sampling parameters of Image features Multinomial dist...\n'

        for c in xrange(clas_num):
            feat_c=[]
            for d in xrange(len(data_c)):
                if data_c[d]==c:
                    feat_c.append(data_feature[d])
            #print repr(j+1)+' '+repr(feat_c)+'\n'

            total_feat=BoF.bag_of_feature(feat_c,FEATURE_DIM)
            total_feat=total_feat+alfa
            fi_Ct[c]=np.random.dirichlet(total_feat)
            if len(feat_c)==0:
                fi_Ct[c]=[float(1.0)/FEATURE_DIM for i in range(FEATURE_DIM)]

        print 'Finished sampling parameters of Image features Multinomial dist...\n'

        #If you estimate space name,you should set Word as True
        #<<<<Sampling word dist parametrer:ramda_ct>>>>>>>>>>>>>>>>>>>>>
        if args.Word:    
            print 'Started sampling parameters of word Multinomial dist...\n'

            
            word_distribusion=[]
            for c in xrange(clas_num):
    		 	
                word_c=[]
                for d in xrange(len(data_c)):
                    if data_c[d]==c:
                        word_c.append(data_word[d])

                total_word=BoF.bag_of_words(word_c,word_class)

                word_distribusion.append(total_word)

                total_word=total_word+beta
                ramda_Ct[c]=np.random.dirichlet(total_word)

                #Not data in class
                if len(word_c)==0:
                    ramda_Ct[c]=[float(1.0)/word_class for i in range(word_class)]

            print 'Finished sampling parameters of Word Multinomial dist...\n'

        # If you use Nonparametric Bayse model,you should set Nonpara as True.
        if args.Nonpara:
            print 'Started sampling parameters of index Multinomial dist...\n'
            #<<<<<Sampling paremeter(pi) of class multinomial dist>>>>>>>>>>>

            class_count=[0 for i in range(clas_num)]

            for c in xrange(clas_num):
                for d in xrange(len(data_c)):
                    if data_c[d]==c:
                        class_count[c] += 1.0
                class_count[c]+= gamma


            pi=np.random.dirichlet(class_count)
            print 'Finished sampling parameters of index Multinomial dist...\n'




        print 'Iteration ',iter+1,' Done..\n'
    C_num=clas_num
    if args.Nonpara:
        C_num=0
        for i in range(len(class_count)):
            if class_count[i]>gamma:
                C_num +=1

        print "Class num:"+repr(C_num)+"\n"
	
    #=====Saving===========================================
    
    makedirs(Out_put_dir)
    makedirs(Out_put_dir+"/mu")
    makedirs(Out_put_dir+"/sigma")
    makedirs(Out_put_dir+"/image_multi")
    makedirs(Out_put_dir+"/class")
    makedirs(Out_put_dir+"/word")
    for i in xrange(clas_num):
        #Writing parameter of positional Gaussian dist
        np.savetxt(Out_put_dir+"/mu/gauss_mu"+repr(i)+".csv",Myu_Ct[i])
        np.savetxt(Out_put_dir+"/sigma/gauss_sgima"+repr(i)+".csv",Sigma_Ct[i])
        #Writing parameter of image features multinomial dist
        np.savetxt(Out_put_dir+"/image_multi/fi_"+repr(i)+".csv",fi_Ct)
        #Writing class indexes
        all=[]
        #k=0
        for r in xrange(len(data_c)):
            if i == data_c[r]:
                r=r+DATA_initial_index
                all.append(r) 
        np.savetxt(Out_put_dir+"/class/class"+repr(i)+".txt",all,fmt="%d")
        if args.Word:
            #Writing parameters of word multinomial dist
            f = open(Out_put_dir+"/word/word_distribution"+repr(i)+'.txt','w')
            for w in xrange(word_class):
                f.write(repr(ramda_Ct[i][w])+"\n")
            f.close()
    #Writing all index
    np.savetxt(Out_put_dir+"/all_class.csv",data_c,fmt="%d")
    
    #saving finish time
    finish_time=time.time()- start_time

    f=open(Out_put_dir+"/time.txt","w")
    f.write("time:"+repr(finish_time)+" seconds.")
    f.close()
    
    #====Writing Parameter===========
    
    f=open(Out_put_dir+"/Parameter.txt","w")

    f.write("max_x_value_of_map: "+repr(MAP_X)+
        "\nMax_y_value_of_map: "+repr(MAP_Y)+
        "\nMin_x_value_of_map: "+repr(map_x)+
        "\nMin_y_value_of_map: "+repr(map_y)+
        "\nNumber_of_place: "+repr(clas_num)+
        "\nData_num: "+repr(Learnig_data_num)+
        "\nSliding_data_parameter: "+repr(Slide)+
        "\nWord_class: "+repr(word_class)+
        "\nDataset: "+data_diric+
        "\nEstimated_place_num: "+repr(C_num)+
        "\nNonparametric_Bayse: "+repr(args.Nonpara)+
        "\nImage_feature_dim: "+repr(FEATURE_DIM)+
        "\nUsing_word_data: "+repr(args.Word)+
        "\nStick_breaking_process_max: "+repr(Stick_large_L)
        )        
    f.close()
    
    f=open(Out_put_dir+"/hyper parameter.txt","w")
    f.write("alfa: "+repr(alfa)+"\n beta: "+repr(beta)
        +("\nkappa_0: ")+repr(kappa_0)+("\nnu_0: ")+repr(nu_0)
        +"\nmu_0: "+repr(mu_0)+"\npsai_0: "+repr(psai_0)+"\ngamma: "+repr(gamma)
        +"\ninitial sigma: "+repr(sigma_init)+"\nsitck break limit: "+repr(Stick_large_L)
        )
    if args.Word:
        f.write("\nspace_name:")
        for i in range(len(space_name)):
            f.write(space_name[i]+",")

    f.write("\nIteration:"+repr(iteration))
    f.close()
    print "%1.3f second"% (finish_time)
    if args.Nonpara:
        np.savetxt(Out_put_dir+"/pi.csv",pi)
    np.savetxt(Out_put_dir+"/initial_mu.csv",initial_mu)
    np.savetxt(Out_put_dir+"/last_mu.csv",Myu_Ct)
    if args.Word:
        f=open(Out_put_dir+"/word_data_class.txt","w")
        f.write("data space_name class\n")
        for j in word_data_ind:
            vec=data_word[j]
            for i in range(len(space_name)):
                if vec[i]!=0:
                    f.write(repr(j+DATA_initial_index)
                        +" "+space_name[i]+" "+repr(data_c[j])+"\n")


if __name__ == '__main__':

    #======================================
    #Reading positional data.
    pose=np.array(f_r.position_data_read(data_diric))

    if CNN_feature==0:
        feature=np.array(f_r.feature_data_read(data_diric))#Reading image feature data
    else:
        feature=np.array(f_r.cnn_feature_data_read(data_diric,S))
    if args.Word:
        word,word_data_ind=f_r.word_data_read(data_diric,DATA_NUM,space_name,DATA_initial_index,word_class,W)
        print word_data_ind
        gibbs(pose,feature,word,word_data_ind)
    else:
        word=[]
        word_data_ind=[]
        gibbs(pose,feature,word,word_data_ind)
