#!/bin/bash

cd /home/parallel/parlab17/lab3/source

export CUDA_VISIBLE_DEVICES=2

if [[ $executable == "kmeans_seq" ]]
then
	./$executable -s $size -n $coord -c $cluster -l $loop 
else
	./$executable -s $size -n $coord -c $cluster -l $loop -b $block_size
fi

