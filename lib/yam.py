# -*- coding:utf-8 -*-

import numpy as np
import sys
import string
dir_=sys.argv[1]
class Yaml:
    def yaml_read(self,file_name):
        data=np.genfromtxt(file_name,dtype= None,delimiter =": ")
        self.file=data[0][1]
        origin_str =str(data[2][1]).translate(string.maketrans("", ""), "[]")
        self.origin=map(float,origin_str.split(", "))
