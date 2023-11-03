#!/bin/bash

queue="parlab"
walltime="23:59:59"
ppn="8"

runs=("1" "2" "3")

# executables=({jacobi,gauss,redblack}-{serial,mpi}-{conv,noconv})
executables=(jacobi-serial-conv)

for run in ${runs[@]}
do
    for exec in ${executables[@]}
    do
        method=$(echo $exec | cut -d"-" -f1)
        version=$(echo $exec | cut -d"-" -f2)
        mode=$(echo $exec | cut -d"-" -f3)

        # TODO: Make more versions for serial
        if [[ $version == "serial" ]]
        then
            if [[ $mode == "debug" ]]
            then
                sizes=("16")
                processes=("1")
            elif [[ $mode == "conv" ]]
            then
                sizes=("1024")
                processes=("1")
            elif [[ $mode == "noconv" ]]
            then
                sizes=("2048 4096 6144")
                processes=("1")
            fi
        elif [[ $version == "mpi" ]]
        then
            if [[ $mode == "debug" ]]
            then
                sizes=("16")
                processes=("64")
            elif [[ $mode == "conv" ]]
            then
                sizes=("1024")
                processes=("64")
            elif [[ $mode == "noconv" ]]
            then
                sizes=("2048 4096 6144")
                processes=("1" "2" "4" "8" "16" "32" "64")
            fi
        fi

        for size in ${sizes[@]}
        do
            for proc in ${processes[@]}
            do
                output="../outputs/${exec}_s${size}_p${proc}_r${run}.out"
                error="../errors/${exec}_s${size}_p${proc}_r${run}.err"

                # ceil($proc/8)
                nodes=$(( ($proc+7) / 8 ))

                # 2^ceil(log2(sqrt($proc)), next 2-power of sqrt(proc)
                # e.g. 8 -> sqrt(8) ~= 2.8
                #   next 2-power: 4
                #   4 x (8/4) = 4x2
                exp=$(echo "l(sqrt($proc))/l(2) + 0.51" | bc -l)
                px=$(echo "2^$exp" | bc 2>/dev/null)
                py=$(echo "$proc/$px" | bc)

                variables="exec=$exec,"
                variables+="size=$size,"
                variables+="proc=$proc,"
                variables+="px=$px,"
                variables+="py=$py,"
                variables+="run=$run"

                command="qsub "
                command+="-q $queue "
                command+="-o $output "
                command+="-e $error "
                command+="-l nodes=$nodes:ppn=$ppn,walltime=$walltime "
                command+="-v $variables "

                if [[ $version == "serial" ]]
                then
                    command+="serialrun.sh"
                else
                    command+="mpirun.sh"
                fi

                $command
            done
        done
    done
done

watch -n 0.1 "queue -d $queue | grep parlab17"
