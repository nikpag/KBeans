#!/bin/bash

cd /home/parallel/parlab17/lab2c/source

export MT_CONF

for thread in $(seq 0 $((10#$numThreads-1)))
do
	if [[ $thread == "64" ]]
	then
		break
	fi

	if [[ $MT_CONF == "" ]]
	then
		MT_CONF+=$thread
	else
		MT_CONF+=,$thread
	fi

	if [[ $numThreads == "128" ]]
	then
		MT_CONF+=,$thread
	fi
done

./$executable $listSize $containsPct $addPct $removePct
