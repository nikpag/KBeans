import glob

time = {}
for filename in sorted(glob.glob('../outputs/Sz*')):

    (
        size,
        coord,
        cluster,
        loop,
        executable,
        block_size,
        ) = tuple(item.split('-')[1] for item in filename.split('.'
                  )[2].split('__'))

    size = int(size)
    coord = int(coord)
    cluster = int(cluster)
    loop = int(loop)
    executable = executable.split('_')[-1]
    block_size = (0 if executable == 'seq' else int(block_size))

    with open(filename) as f:
        for line in f:
            if line.startswith('analysis'):
                analysis = line.split()
                gpu = analysis[3]
                transfer = analysis[7]
                cpu = analysis[11]
                cal_time_dict = {'gpu': gpu, 'transfer': transfer,
                                 'cpu': cpu}
                time.setdefault(executable, {}).setdefault(coord,
                        {})[block_size] = cal_time_dict

coords = [2,16]
block_sizes = [32, 64, 128, 256, 512, 1024] 
executables = ['naive', 'transpose', 'shared'] 
    
for feature in coords:
    filename = f"../tables/c-{feature}.tex"
    with open(filename, "w") as f:
            def printfile(s):
                print(s, file=f)
            printfile(f"\\begin{{center}}")
            printfile(f"\\begin{{tblr}}{{c c c c c}}")
            printfile(f"\\hline")
            printfile(f"Executable &  Block Size  & gpu & transfer & cpu\\\\")
            printfile(f"\\hline")
            for executable in executables:
                printfile(f"\\SetCell[r=6]{{}} ")
                for block_size in block_sizes: 
                    line_time = list(time[executable][feature][block_size].values())
                    if (block_size==32): 
                        printfile(f"{executable} & {block_size} & {line_time[0]} & {line_time[1]} & {line_time[2]} \\\\")
                    else: 
                        printfile(f"& {block_size} & {line_time[0]} & {line_time[1]} & {line_time[2]} \\\\")
                printfile(f"\\hline")
            printfile(f"\\end{{tblr}}")
            printfile(f"\\end{{center}}")

























