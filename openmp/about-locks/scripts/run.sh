#!/bin/bash

module load openmp
cd /home/parallel/parlab17/lab2.5/source

if [[ $affinity != "0" ]]
then
	export GOMP_CPU_AFFINITY=$affinity
fi

export OMP_NUM_THREADS=$threads
./$executable -s $size -n $coords -c $clusters -l $loops
