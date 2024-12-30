#!/bin/bash

# compile to c
cython --embed -o ./build/password.c password.py

# create an executable
gcc -v -I /Users/wes/.pyenv/versions/3.12.0/include/python3.12 -L /usr/local/Frameworks/Python.framework/Versions/3.12/lib -o./build/password ./build/password.c -lpython3.12 -lpthread -lm -lutil -ldl
