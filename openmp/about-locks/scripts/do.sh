#!/bin/bash

queue="serial"
size="16"
loops="10"

bash qsub-make.sh $queue
bash qsub-run-all.sh $queue $size $loops
