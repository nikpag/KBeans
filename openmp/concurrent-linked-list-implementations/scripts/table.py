import glob

print("Started")

throughput = {}

for filename in sorted(glob.glob("../outputs/x.*.out")):
	executable, list_size, contains, add, remove, threads = filename.split("-")

	executable = executable.split("/")[-1]
	list_size = int(list_size[1:])
	workload = tuple(int(item[1:]) for item in (contains, add, remove))
	threads = int(threads[1:4])

	with open(filename) as f:
		for line in f:
			if line.startswith("Nthreads"):
				throughput \
					.setdefault(executable, {}) \
					.setdefault(list_size, {}) \
					.setdefault(workload, {})[threads] = float(line.split()[7])

# No x.serial here. This is by design
executables = ["x.serial", "x.cgl", "x.fgl", "x.opt", "x.lazy", "x.nb"]
list_sizes = [1024, 8192]
workloads = [(100, 0, 0), (80, 10, 10), (20, 40, 40), (0, 50, 50)]
threads = [1, 2, 4, 8, 16, 32, 64, 128]
print("Throughput okay")

for list_size in list_sizes:
	for workload in workloads:
		contains, add, remove = workload

		filename = f"../graphs/s{list_size}-c{contains}-a{add}-r{remove}.tex"
		with open(filename, "w") as f:
			def printfile(s):
				print(s, file=f)

			printfile(f"\\begin{{center}}")
			printfile(f"\\textbf{{Throughput for List Size: {list_size}, Contains: {contains}\\%, Add: {add}\\%, Remove: {remove}\\% (Kops/sec)}}")
			printfile(f"\\begin{{tabular}}{{|c|c|c|c|c|c|c|}}")

			printfile(f"\\hline")
			printfile(f"\\diagbox{{Threads}}{{Executable}} & \\verb|x.serial| & \\verb|x.cgl| & \\verb|x.fgl| & \\verb|x.opt| & \\verb|x.lazy| & \\verb|x.nb| \\\\")
			printfile(f"\\hline")

			for thread in threads:
				if thread != 1:
					throughput["x.serial"][list_size][workload][thread] = ""
				l = [ throughput[executable][list_size][workload][thread] for executable in executables]
				printfile(f"{thread} & {l[0]} & {l[1]} & {l[2]} & {l[3]} & {l[4]} & {l[5]} \\\\")
				printfile(f"\\hline")

			printfile(f"\\end{{tabular}}")
			printfile(f"\\end{{center}}")
