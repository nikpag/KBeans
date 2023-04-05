#!/bin/bash

queue="serial"
nodes="dungani"

runPPN="8"
runWalltime="00:00:30"

# executables=("kmeans_seq" "kmeans_cuda_naive" "kmeans_cuda_transpose" "kmeans_cuda_shared" "kmeans_cuda_all_gpu")
executables=("kmeans_cuda_naive" "kmeans_cuda_transpose" "kmeans_cuda_shared")

# sizes="256"
sizes="256"

# coords="2 16"
coords="2 16"

# clusters="16"
clusters="16"

# loops="10"
loops="10"

# block_sizes="32 64 128 256 512 1024"
block_sizes="32 64 128 256 512 1024"

for size in $sizes
do
    for coord in $coords
    do
        for cluster in $clusters
        do
            for loop in $loops
            do
                filename="../source/Execution_logs/Sz-${size}_Coo-${coord}_Cl-${cluster}.csv"
                echo "Implementation,blockSize,av_loop_t,min_loop_t,max_loop_t" > $filename

                for executable in ${executables[@]}
                do
                    for block_size in $block_sizes
                    do
                        if [[ $executable == "kmeans_seq" && $block_size != "32" ]]
                        then 
                            continue
                        fi
                        
                        runOutput="../outputs/Sz-${size}__Coo-${coord}__Cl-${cluster}__Loo-${loop}__Exe-${executable}__Bl-${block_size}.out"
                        runError="../errors/Sz-${size}__Coo-${coord}__Cl-${cluster}__Loo-${loop}__Exe-${executable}__Bl-${block_size}.err"

                        variables=""
                        variables+="executable=$executable,"
                        variables+="size=$size,"
                        variables+="coord=$coord,"
                        variables+="cluster=$cluster,"
                        variables+="loop=$loop,"
                        variables+="block_size=$block_size"

                        qsubRunCommand=""
                        qsubRunCommand+="qsub "
                        qsubRunCommand+="-q $queue "
                        qsubRunCommand+="-o $runOutput "
                        qsubRunCommand+="-e $runError "
                        qsubRunCommand+="-l nodes=$nodes:ppn=$runPPN,walltime=$runWalltime "
                        qsubRunCommand+="-v $variables "
                        qsubRunCommand+="run.sh"

                        $qsubRunCommand
                    done
                done
            done
        done
    done
done   

watch -n 0.1 "queue -d $queue | grep parlab17"