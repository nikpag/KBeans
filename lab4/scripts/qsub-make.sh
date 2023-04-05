#!/bin/bash

queue="parlab"
nodes="1"

output="../outputs/make.out"
error="../errors/make.err"
ppn="1"
walltime="00:00:30"

command="qsub "
command+="-q $queue "
command+="-o $output "
command+="-e $error "
command+="-l nodes=$nodes:ppn=$ppn,walltime=$walltime "
command+="make.sh"

$command

watch -n 0.1 "stat -c %Y $output"
