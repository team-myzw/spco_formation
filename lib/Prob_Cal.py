#!/usr/bin/env python
import sys
import math
import numpy as np
from numpy.linalg import inv, cholesky
from scipy.stats import chi2
sys.path.append("multi_dist/")
import Multi
def normalize(probs):
    prob_factor = 1.0 / sum(probs)
    return [prob_factor * p for p in probs]


def multi_nomial(vec,phi):
    vec=vec.tolist()
    phi=phi.tolist()

    n=int(sum(vec))
    ans=Multi.multinomial(phi,vec,n)
    ans=math.exp(ans)

    return ans

#====Caluculating probability using multinomial distribution. 
def multi_nomial_log(vec,phi):
    vec=vec.tolist()
    phi=phi.tolist()

    n=int(sum(vec))
    ans=Multi.multinomial(phi,vec,n)
    #ans=math.exp(ans)

    return ans


def multi_gaussian(x_t,mu_t,sigma_t):
    x_matrix =np.matrix(x_t)
    mu =np.matrix(mu_t)
    sigma =np.matrix(sigma_t)
    a = np.sqrt(np.linalg.det(sigma)*(2*np.pi)**sigma.ndim)
    a=math.log(a)
    #print sigma.I
    b = np.linalg.det(-0.5*((x_matrix-mu)*inv(sigma)*(x_matrix-mu).T))
    
    return math.exp(b-a)



def multi_gaussian_log(x_t,mu_t,sigma_t):
    x_matrix =np.matrix(x_t)
    mu =np.matrix(mu_t)
    sigma =np.matrix(sigma_t)
    a = np.sqrt(np.linalg.det(sigma)*(2*np.pi)**sigma.ndim)
    a=math.log(a)
    #print sigma.I
    b = np.linalg.det(-0.5*((x_matrix-mu)*inv(sigma)*(x_matrix-mu).T))
    
    return b-a



#========Sampling from Wishart distribution========================================
def sampling_wishart(nu, W):
    dim = W.shape[0]
    #print W
    chol = cholesky(W)

    foo = np.zeros((dim,dim))
    for i in xrange(dim):
        for j in xrange(i+1):
            if i == j:
                foo[i,j] = np.sqrt(chi2.rvs(nu-(i+1)+1))
            else:
                foo[i,j]  = np.random.normal(0,1)

    return np.dot(chol, np.dot(foo, np.dot(foo.T, chol.T)))
#==========Sampling from inverse Wishart distribution===================================================================
def sampling_invwishartrand(nu,W):
    return inv(sampling_wishart(nu,inv(W)))