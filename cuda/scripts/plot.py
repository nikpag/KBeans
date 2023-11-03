import glob
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

data = {}

for filename in sorted(glob.glob("../outputs/Sz*")):
	(size,
	 coord,
	 cluster,
	 loop,
	 executable,
	 block_size) = tuple(item.split("-")[1] for item in filename.split(".")[2].split("__"))

	size = int(size)
	coord = int(coord)
	cluster = int(cluster)
	loop = int(loop)
	executable = executable.split("_")[-1]
	block_size = 0 if executable == "seq" else int(block_size)

	with open(filename) as f:
		for line in f:
			if line.startswith("nloops"):
				data \
					.setdefault(coord, {}) \
					.setdefault(executable, {}) \
					.setdefault(block_size, {})["time"] \
						= float(line.split()[6])
	
for coord in data:
		for executable in data[coord]:
			for block_size in data[coord][executable]:
				sequential = data[coord]["seq"][0]["time"]
				parallel = data[coord][executable][block_size]["time"]
				data[coord][executable][block_size]["speedup"] = sequential / parallel

ax_number = {"time": 0, "speedup": 1}
title = {"time": "Execution time", "speedup": "Speedup"}
xlabel = "Block size"
ylabel = {"time": "Time (ms)", "speedup": "Speedup"}
xticks = {"time": [0, 1, 2, 3, 4, 5, 6], "speedup": [0, 1, 2, 3, 4, 5]}
xticklabels = {
	"time": ["seq", "32", "64", "128", "256", "512", "1024"],
	"speedup": ["32", "64", "128", "256", "512", "1024"]
}
coords = [2, 16]
block_sizes = [32, 64, 128, 256, 512, 1024]
# executables_list = [ ["naive"], ["naive", "transpose"], ["naive", "transpose", "shared"] ]
executables_list = [ ["naive", "transpose", "shared"] ]
color = {
	"time": {
		"seq": "#242424",
		"naive": "darkred",
		"transpose": "orangered",
		"shared": "darkorange",
	},
	"speedup": {
		"naive": "lightgreen",
		"transpose": "limegreen",
		"shared": "darkgreen"
	}
}

for coord in coords:
	for executables in executables_list:
		figw, figh = plt.rcParams["figure.figsize"]
		fig, axes = plt.subplots(2, 1, figsize=(0.9*figw, 2*figh))

		for resource in ["time", "speedup"]:
			ax = axes[ax_number[resource]]
			ax.set_title(title[resource])
			ax.grid()
			ax.set_xlabel(xlabel)
			ax.set_ylabel(ylabel[resource])
			ax.set_xticks(ticks=xticks[resource], labels=xticklabels[resource])
			ax.set_axisbelow(True)

			n = len(executables)
			w = 0.4 / n ** 0.5
			offset = -(n-1) * w/2

			if resource == "time":
				ax.bar(
					x=xticks[resource][0],
					height=data[coord]["seq"][0][resource],
					width=w,
					label="seq",
					color=color[resource]["seq"]
				)

			for executable in executables:
				# height = [ data[coord]["seq"][0][resource] ] if resource == "time" else []
				start = 1 if resource == "time" else 0
				x = [xtick + offset for xtick in xticks[resource][start:]]
				height = [
					data[coord][executable][block_size][resource]
						for block_size in block_sizes
				]

				ax.bar(
					x=x,
					height=height,
					width=w,
					label=executable,
					color=color[resource][executable]
				)

				ax.legend()
				ax.set_ylim([0, 1.2*max([data[coord]["seq"][0][resource]] + height)])
				offset += w

		plt.tight_layout(h_pad=5)
		filename = f"../graphs/{coord}-{'-'.join(executables)}.pdf"
		plt.savefig(filename)
		plt.close()
