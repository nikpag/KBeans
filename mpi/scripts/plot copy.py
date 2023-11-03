from glob import glob
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

data = {}
filenames = [filename for filename in glob("../outputs/*") if filename != "../outputs/make.out"]

for filename in filenames:
    (exec,
     size,
     proc,
     run) = tuple(item for item in filename.split("/")[2].split('.'))[0].split('_')

    size = int(size[1:])
    proc = int(proc[1:])
    run = int(run[1:])
    serial = True if "serial" in exec else False

    # MAYBE: Check for conv and noconv
    exec = '-'.join(exec.split('-')[:1])

    with open(filename) as f:
        line = f.readline()
        if not serial:
            data \
                .setdefault(size, {}) \
                .setdefault(exec, {}) \
                .setdefault(proc, {}) \
                .setdefault(run, {})["time"] \
                    = (float(line.split()[12]),float(line.split()[14]), float(line.split()[16]))
        else:
            data \
                .setdefault(size, {}) \
                .setdefault(exec, {}) \
                .setdefault(proc, {}) \
                .setdefault(run, {})["stime"] \
                    = float(line.split()[8])
# print(data)
for size in data:
    for exec in data[size]:
        for proc in data[size][exec]:
            if size == 1024:
                break
            sequential = 0; par_tt=0; par_comt=0; par_cont=0
            for run in range(1,4):
                sequential += data[size][exec][1][run]["time"][2]
                par_comt += data[size][exec][proc][run]["time"][0]
                par_cont += data[size][exec][proc][run]["time"][1]
                par_tt += data[size][exec][proc][run]["time"][2]
            #μπορούμε εδώ να προσθέσουμε κάποιον έλεγχο για outliers
            data[size][exec][proc]["mtime"] = (round(par_comt/3,6), round(par_cont/3,6), round(par_tt/3,6))
            data[size][exec][proc]["speedup"] = round((sequential/3)/(par_tt/3),6)
        # data[size][exec]["mean-serial"] = round(sequential/3,6)
print(data)

ax_number = {"mtime": 0, "speedup": 1}
title = {"mtime": "Execution time", "speedup": "Speedup"}
xlabel = ""
ylabel = {"mtime": "Time (ms)", "speedup": "Speedup"}
xticks = {"mtime": [1, 2, 3, 4], "speedup": [0, 1, 2, 3, 4, 5, 6]}
xticklabels = {
	"mtime": ["8", "16", "32", "64"],
	"speedup": ["1","2", "4", "8", "16", "32", "64"]
}

sizes= [2048, 4096, 6144]
proc= [1, 2, 4, 8, 16, 32, 64]
exec_list = [ ["jacobi", "gauss", "redblack"] ]

# θα τα αλλάξουμε τα χρώματα μην μου αγχώνεσαι
color = {
	"mtime": {
		"seq": "#242424",
		"jacobi": "darkred",
		"gauss": "orangered",
	},
	"speedup": {
		"jacobi": "lightgreen",
		"gauss": "limegreen",
        "redblack": "darkgreen"
	}
}

for size in sizes:
    for executables in exec_list:
        figw, figh = plt.rcParams["figure.figsize"]
        fig, axes = plt.subplots(2, 1, figsize=(0.9*figw, 2*figh))

        for resource in ["speedup"]:
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

            # if resource == "time":
            #     ax.bar(
			# 		x=xticks[resource][0],
			# 		height=data[size][executables]["mean-serial"],
			# 		width=w,
			# 		label="seq",
			# 		color=color[resource]["seq"]
			# 	)

            for executable in executables:
				# height = [ data[coord]["seq"][0][resource] ] if resource == "time" else []
                start=0
                x = [xtick + offset for xtick in xticks[resource][start:]]

                height = [
					data[size][executable][p][resource]
						for p in proc
				]
                # if resource == "mtime":
                #     print(height)

                ax.bar(
					x=x,
					height=height,
					width=w,
					label=executable,
					color=color[resource][executable]
				)

                ax.legend()
                # ax.set_ylim([0, 1.2*max([data[coord]["seq"][0][resource]] + height)])
                offset += w

        plt.tight_layout(h_pad=5)
        filename = f"../graphs/time-{size}.pdf"
        plt.savefig(filename)
        plt.close()
