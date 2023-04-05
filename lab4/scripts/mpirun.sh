#!/bin/bash

cd /home/parallel/parlab17/lab4/source

export TMPDIR=$HOME/tmp/${exec}_s${size}_p${proc}_r${run}

mkdir -p $TMPDIR

module load openmpi/1.8.3

mpirun -np $proc --mca btl self,tcp --map-by node ./$exec $size $size $px $py

rm -rf $TMPDIR
