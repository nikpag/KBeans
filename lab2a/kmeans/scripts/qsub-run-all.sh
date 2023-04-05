#!/bin/bash

queue=$1
size=$2
loops=$3

configs="sequential|kmeans_seq|16|16|0 \
naive-no-aff|kmeans_omp_naive|16|16|0 \
naive-aff|kmeans_omp_naive|16|16|1 \
reduction-easy|kmeans_omp_reduction|16|16|1 \
reduction-hard-no-fs|kmeans_omp_reduction|1|4|1 \
reduction-hard-fs|kmeans_omp_reduction_fs|1|4|1 \
reduction-numa-hard|kmeans_omp_reduction_numa|1|4|1 \
reduction-numa-easy|kmeans_omp_reduction_numa|16|16|1"

configs="sequential-easy|kmeans_seq|16|16|0 \
sequential-hard|kmeans_seq|1|4|0"

threadsList="1 2 4 8 16 32 64"

for config in $configs
do
	output=$(echo $config | cut -d"|" -f1)
	executable=$(echo $config | cut -d"|" -f2)
	coords=$(echo $config | cut -d"|" -f3)
	clusters=$(echo $config | cut -d"|" -f4)
	haveAffinity=$(echo $config | cut -d"|" -f5)
	actualThreadsList=$([[ "$executable" == "kmeans_seq" ]] && echo "1" || echo $threadsList)

	for threads in $actualThreadsList
	do
		affinity=0
		if [[ "$haveAffinity" == "1" ]]
		then
			affinity="0-$(($threads-1))"
		fi
		if [[ "$affinity" == "0-0" ]]
		then
			affinity="0"
		fi
		bash qsub-run.sh $queue $output $executable $size \
			$coords $clusters $loops $threads $affinity
	done
done

watch -n 0.1 "queue -d $queue | grep parlab17"
