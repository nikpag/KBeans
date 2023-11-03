#!/bin/bash

queue=$1
output="../outputs/$2"
error="../errors/$2"
executable=$3
size=$4
coords=$5
clusters=$6
loops=$7
threads=$8
affinity=$9

output=$output-$threads
error=$error-$threads

nodes=$([[ "$queue" == "serial" ]] && echo "sandman" || echo "1")
ppn=$([[ "$queue" == "serial" ]] && echo "64" || echo "8")
walltime="00:00:30"

variables="executable=$executable,\
size=$size,\
coords=$coords,\
clusters=$clusters,\
loops=$loops,\
threads=$threads,\
affinity=$affinity"

qsub \
	-q $queue \
	-o $output.out \
	-e $error.err \
	-l nodes=$nodes:ppn=$ppn,walltime=$walltime \
	-v $variables \
	run.sh
