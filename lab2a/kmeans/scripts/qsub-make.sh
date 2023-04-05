#!/bin/bash

queue=$1

output="../outputs/make"
error="../errors/make"
nodes=$([[ "$queue" == "serial" ]] && echo "sandman" || echo "1")
ppn="1"
walltime="00:00:30"

qsub \
	-q $queue \
	-o $output.out \
	-e $error.err \
	-l nodes=$nodes:ppn=$ppn,walltime=$walltime \
	make.sh

watch -n 0.1 "stat -c %Y $output.out"
