#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_Game_Of_Life

## Output and error files
#PBS -o run_Game_Of_Life.out
#PBS -e run_Game_Of_Life.err

## How many machines should we get?
#PBS -l nodes=1:ppn=8

## How long should the job run for?
#PBS -l walltime=00:10:00

## Start
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab17/lab1

export OMP_NUM_THREADS

for OMP_NUM_THREADS in 1 2 4 6 8
do
	echo Using $OMP_NUM_THREADS threads
	./Game_Of_Life 64 1000
	./Game_Of_Life 1024 1000
	./Game_Of_Life 4096 1000
	echo
done
