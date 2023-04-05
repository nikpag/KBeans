import glob
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

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
executables = ["x.cgl", "x.fgl", "x.opt", "x.lazy", "x.nb"]
list_sizes = [1024, 8192]
workloads = [(100, 0, 0), (80, 10, 10), (20, 40, 40), (0, 50, 50)]
threads = [1, 2, 4, 8, 16, 32, 64, 128]

for list_size in list_sizes:
	for workload in workloads:
		figw, figh = plt.rcParams["figure.figsize"]
		plt.figure(figsize=(figw, figh))
		contains, add, remove = workload
		plt.title(f"List Size: {list_size}, Contains: {contains}% Add: {add}% Remove: {remove}%")
		plt.grid(True, zorder=0)
		plt.xlabel("Threads")
		plt.ylabel("Throughput (Kops/sec)")
		plt.xticks(range(len(threads)), threads)
		n = len(executables)
		w = 0.8 / n
		offset = -(n-1) * w/2
		colors = [f"tab:{color}" for color in ["blue", "orange", "purple", "green", "red"]]

		for color_num, executable in enumerate(executables):
			sequential = throughput["x.serial"][list_size][workload][1]

			plt.axhline(sequential, linewidth=8*w, color="tab:red", zorder=0)
			plt.bar(
				np.arange(len(threads)) + offset,
				height=[ throughput[executable][list_size][workload][thread] for thread in threads ],
				width=w,
				label=executable,
				zorder=2,
				color=colors[color_num]
			)

			offset += w

		plt.legend()
		filename = f"../graphs/s{list_size}-c{contains}-a{add}-r{remove}.pdf"
		plt.savefig(filename)
		plt.close()
