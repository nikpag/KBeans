#!/bin/bash

# For local use only! (not scirouter)

name=jacobi-mpi

cd ~/scirouter-dir/lab4/source/

mpicc -O3 -Wall -DTEST_CONV $name.c utils.c -o $name -lm

mpirun -np 1 --mca btl self,tcp --map-by node ./$name 1024 1024 1 1
