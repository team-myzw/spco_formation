# Makefile
multi: multi.c multiWrapper.c
	gcc -fpic -o multi.o -c multi.c
	gcc -fpic -I/usr/include/python -o multiWrapper.o -c multiWrapper.c
	gcc -shared multi.o multiWrapper.o -o multimodule.so
