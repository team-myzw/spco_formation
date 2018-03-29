// helloWrap.c
#include <python2.7/Python.h>
#include<math.h>
#include<stdlib.h> 
#define feature_num 3

double factorial(double value){
  if(value>0){
    return log(value)+factorial(value-1);
  }else{return 0;}
  
}


static PyObject * 
multinomial(PyObject* self, PyObject* args){
  //unsigned int min,max;
  
  int sum,i,j,n;
  PyObject *get_list,*get_list2;
  
  if (PyArg_ParseTuple(args, "OOi",&get_list,&get_list2,&sum)){ 
    int len=PyList_Size(get_list);
    double phi[len],vec[len];
      //n=PyList_Size(get_list);
      if PyList_Check(get_list) {
      for (i=0; i<len; i++){
    
    phi[i] =PyFloat_AsDouble( PyList_GetItem(get_list, (Py_ssize_t)i));
    vec[i] =PyInt_AsSsize_t( PyList_GetItem(get_list2, (Py_ssize_t)i));
      }
    }
  

  double prob=factorial(sum);
  double left=0,right=0;
  for(i=0;i<len;i++){
    left+=factorial(vec[i]);
    n=0;
    for(j=0;j<vec[i];j++){
      n++;
      right +=log(phi[i]);

    }
  }
  prob=prob-left + right;
  
    return Py_BuildValue("d",prob);
  }else{return Py_BuildValue("");}

}

/*
static PyObject * 
multinomial(PyObject* self, PyObject* args){
  double value;
  if (PyArg_ParseTuple(args, "d",&value)){ 
    value=factorial(value);
    return Py_BuildValue("d",value);
  }else{return Py_BuildValue("");}

}*/
 

static PyMethodDef multimethods[] = {
  {"multinomial", multinomial, METH_VARARGS,"return prob.\n"},
  {NULL},
};
 
 
void initMulti(void){
  Py_InitModule("Multi", multimethods);
}

