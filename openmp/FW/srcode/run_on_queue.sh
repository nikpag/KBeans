#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_fw

## Output and error files
#PBS -o run_naive.out
#PBS -e run_naive.err

## How many machines should we get?
#PBS -l nodes=1:ppn=8

##How long should the job run for?
#PBS -l walltime=00:30:00

## Start
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab17/lab2/FW

export OMP_NUM_THREADS

#echo FW: Serial version

#for SIZE in 1024 2048 4096
#do
#	for i in 1 2 4 8 16 32 64
#	do 
#		export OMP_NUM_THREADS=$i
#		./fw $SIZE
#	done
#done

# TODO: figure out what BSIZE should be (leave default?)

#echo FW: Recursive version
export OMP_NESTED=TRUE

for i in 1024 2048 4096
do 
	for j in 16 256 512 
	do	
		for z in 1 2 4 8 16 32 64 
		do 
			export OMP_NUM_THREADS=$z 
			./fw_sr $i $j
		done
	done
done
 
#for i in 1 2 4 8 16 32 64
#do
#	for SIZE in 2048
#	do
#		export OMP_NUM_THREADS=$i
#		echo "Number of threads: $i"
#		./fw_sr $SIZE 32
#		./fw_sr $SIZE 64
#		./fw_sr $SIZE 128
#		./fw_sr $SIZE 256
#		./fw_sr $SIZE 512		
#	done
#done

#echo FW: Tiled version

#for i in 1024 2048 4096
#do
#	for j in 32 64 128 256 512
#	do 
#		for z in 1 2 4 8 16 32 64 
#		do
#			export OMP_NUM_THREADS=$z
#			./fw_tiled $i $j 
#		done
#	done
#done
