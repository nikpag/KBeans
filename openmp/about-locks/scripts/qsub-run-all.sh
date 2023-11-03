#!/bin/bash

queue=$1
size=$2
loops=$3

configs="\
kmeans_seq|kmeans_seq|16|16|0 \
kmeans_omp_array_lock|kmeans_omp_array_lock|16|16|1 \
kmeans_omp_clh_lock|kmeans_omp_clh_lock|16|16|1 \
kmeans_omp_critical|kmeans_omp_critical|16|16|1 \
kmeans_omp_naive|kmeans_omp_naive|16|16|1 \
kmeans_omp_nosync_lock|kmeans_omp_nosync_lock|16|16|1 \
kmeans_omp_pthread_mutex_lock|kmeans_omp_pthread_mutex_lock|16|16|1 \
kmeans_omp_pthread_spin_lock|kmeans_omp_pthread_spin_lock|16|16|1 \
kmeans_omp_tas_lock|kmeans_omp_tas_lock|16|16|1 \
kmeans_omp_ttas_lock|kmeans_omp_ttas_lock|16|16|1\
"

threadsList="01 02 04 08 16 32 64"

for config in $configs
do
	output=$(echo $config | cut -d"|" -f1)
	executable=$(echo $config | cut -d"|" -f2)
	coords=$(echo $config | cut -d"|" -f3)
	clusters=$(echo $config | cut -d"|" -f4)
	haveAffinity=$(echo $config | cut -d"|" -f5)
	actualThreadsList=$([[ "$executable" == "kmeans_seq" ]] && echo "01" || echo $threadsList)

	for threads in $actualThreadsList
	do
		affinity=0
		if [[ "$haveAffinity" == "1" ]]
		then
			affinity="0-$((10#$threads-1))"
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
