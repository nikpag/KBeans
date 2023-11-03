#!/bin/bash

queue="serial"
size="256"
loops="10"

bash qsub-make.sh $queue
bash qsub-run-all.sh $queue $size $loops
