queue="serial"
nodes="sandman"

makeOutput="../outputs/make.out"
makeError="../errors/make.err"
makePPN="1"
makeWalltime="00:00:30"

qsub \
	-q $queue \
	-o $makeOutput \
	-e $makeError \
	-l nodes=$nodes:ppn=$makePPN,walltime=$makeWalltime \
	make.sh

watch -n 0.1 "stat -c %Y $makeOutput"

runPPN="64"
runWalltime="00:00:30"

executables="x.cgl x.fgl x.lazy x.nb x.opt x.serial"
threads="001 002 004 008 016 032 064 128"
listSizes="1024 8192"
configs="100-0-0 80-10-10 20-40-40 0-50-50"

for executable in $executables
do
	for thread in $threads
	do
		for listSize in $listSizes
		do
			for config in $configs
			do
				containsPct=$(echo $config | cut -d"-" -f1)
				addPct=$(echo $config | cut -d"-" -f2)
				removePct=$(echo $config | cut -d"-" -f3)

				runOutput="../outputs/$executable-s$listSize-c$containsPct-a$addPct-r$removePct-t$thread.out"
				runError="../errors/$executable-s$listSize-c$containsPct-a$addPct-r$removePct-t$thread.err"

				variables=""
				variables+="numThreads=$thread,"
				variables+="executable=$executable,"
				variables+="listSize=$listSize,"
				variables+="containsPct=$containsPct,"
				variables+="addPct=$addPct,"
				variables+="removePct=$removePct"

				qsubCommand=""
				qsubCommand+="qsub "
				qsubCommand+="-q $queue "
				qsubCommand+="-o $runOutput "
				qsubCommand+="-e $runError "
				qsubCommand+="-l nodes=$nodes:ppn=$runPPN,walltime=$runWalltime "
				qsubCommand+="-v $variables "
				qsubCommand+="run.sh"

				if [[ $executable == "x.serial" && $thread != "001" ]]
				then
					continue
				fi

				$qsubCommand
			done
		done
	done
done

watch -n 0.1 "queue -d $queue | grep parlab17"
