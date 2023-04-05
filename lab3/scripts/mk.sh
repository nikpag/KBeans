#!/bin/bash

queue="serial"
nodes="dungani"

makeOutput="../outputs/make.out"
makeError="../errors/make.err"
makePPN="1"
makeWalltime="00:00:30"

qsubMakeCommand=""
qsubMakeCommand+="qsub "
qsubMakeCommand+="-q $queue "
qsubMakeCommand+="-o $makeOutput "
qsubMakeCommand+="-e $makeError "
qsubMakeCommand+="-l nodes=$nodes:ppn=$makePPN,walltime=$makeWalltime "
qsubMakeCommand+="make.sh"

$qsubMakeCommand

watch -n 0.1 "stat -c %Y $makeOutput"