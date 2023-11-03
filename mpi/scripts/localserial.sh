#!/bin/bash

# For local use only! (not scirouter)

name=jacobi-serial

cd ~/scirouter-dir/lab4/source/

gcc -O3 -Wall -DTEST_CONV $name.c utils.c -o $name -lm

./$name 1024 1024
