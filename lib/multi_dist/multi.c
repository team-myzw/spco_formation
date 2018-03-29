// hello.c
#include <stdio.h>
#include <math.h>
#include <python2.7/Python.h>
#include <stdlib.h> 


int add(int x, int y){
return x + y;
}
 
void out(const char* adrs, const char* name){
  printf("hello, my name is %s %s.\n", adrs, name);
}
