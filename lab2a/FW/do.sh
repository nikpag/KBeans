#! /bin/bash

rm *.{err,out} &&
qsub -q parlab make_on_queue.sh &&
watch -n 0.1 "ls | grep make*.err" &&
qsub -q serial -l nodes=sandman:ppn=64 run_on_queue.sh &&
watch -n 0.1 "ls | grep run*.err"
