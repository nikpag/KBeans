#!/bin/bash

export TMPDIR=$HOME/tmp/make

mkdir -p $TMPDIR

module load openmpi/1.8.3
cd /home/parallel/parlab17/lab4/source
make

rm -rf $TMPDIR
