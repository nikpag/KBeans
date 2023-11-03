from glob import glob
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

data = {}
filenames = [filename for filename in glob("../outputs/*") if filename != "../outputs/make.out"]

for filename in filenames:
    nodir = filename.split("/")[2]
    noext = nodir.split(".")[0]
    items = noext.split("_")

    exec, size, proc, run = items

    method, version, mode = exec.split("-")
    size = int(size[1:])
    proc = int(proc[1:])
    run = int(run[1:])

    with open(filename) as f:
        line = f.readline()

        tlabels = {
            "serial": [("ttotal", 8)],
            "mpi": [("tcomp", 12), ("tconv", 14), ("ttotal", 16)]
        }

        for tname, tsplit in tlabels[version]:
            data.setdefault(method, {}) \
                .setdefault(version, {}) \
                .setdefault(mode, {}) \
                .setdefault(size, {}) \
                .setdefault(proc, {}) \
                .setdefault(run, {}) \
                .setdefault(tname, float(line.split()[tsplit]))

for method in data:
    for version in data[method]:
        for mode in data[method][version]:
            for size in data[method][version][mode]:
                for proc in data[method][version][mode][size]:
                    for tname in data[method][version][mode][size][proc][1]:
                        data[method][version][mode][size][proc][1][tname] = (
                            np.mean([data[method][version][mode][size][proc][r][tname] for r in [1, 2, 3]])
                        )

                    data[method][version][mode][size][proc][1]["speedup"] = (
                        data[method]["mpi"][mode][size][1][1]["ttotal"] /
                        data[method][version][mode][size][proc][1]["ttotal"]
                    )

color = {
    "time": {
        "tcomp": "firebrick",
        "tconv": "darkorange",
        "ttotal": "sandybrown",
    },
    "speedup": {
        "jacobi": "lightgreen",
        "gauss": "limegreen",
        "redblack": "forestgreen"
    }
}

configs = {
    "time-conv": {
        "sizes": [1024],
        "title": "Time, conv",
        "xlabel": "Method",
        "ylabel": "Time (sec)",
        "xticks": ["Jacobi", "Gauss", "RedBlack"],
        "colors":

    },
    "speedup-noconv": {
        "sizes": [2048, 4096, 6144],
        "title": "Speedup, noconv",
        "xlabel": "#Processes",
        "ylabel": "Speedup",
        "xticks": ["1", "2", "4", "8", "16", "32", "64"]
        "colors":

    },
    "time-noconv": {
        "sizes": [2048, 4096, 6144],
        "title": "Time, noconv",
        "xlabel": "Method_Processes",
        "ylabel": "Time (sec)",
        "xticks": []
        "colors":
    }
}

for k, config in configs.items():
    for size in config["sizes"]:
        figw, figh = plt.rcParams["figure.figsize"]
        plt.figure(figsize=(figw, figh))
        plt.title(config["title"])
        plt.grid(True, zorder=0)

        plt.xlabel(config["xlabel"])
        plt.ylabel(config["ylabel"])

        xticks = config["xticks"]

        plt.xticks(range(len(xticks)), xticks)

        height =


#### COMMON CODE ####

for tname in ["tcomp", "tconv", "ttotal"]:
        height = data[method][version][mode][size][proc][run][tname]

        plt.bar(
            np.arange(len(xticks)),
            height=height,
            width=0.1,
            label=tname,
            zorder=2,
            color=color["time"][tname]
        )

###
    n = len(methods)
    w = 0.4 / n ** 0.5
    offset = -(n-1) * w/2
###

        plt.legend()

        offset += w

    plt.tight_layout(h_pad=5)
    filename = f"../graphs/speedup-{size}.pdf"
    plt.savefig(filename)
    plt.close()


# Time, Convergence, size=1024, proc=64, ttotal,conv,comp
size = 1024
proc = 64

methods = ["Jacobi", "Gauss", "RedBlack"]

for method in methods:
    plt.figure(figsize=(figw, figh))
    plt.title(f"{method}, convergence, 1024x1024, 64 processes")
    plt.grid(True, zorder=0)
    plt.xlabel("Method")
    plt.ylabel("Time (sec)")
    xticks = methods
    plt.xticks(range(len(xticks)), xticks)

    for tname in ["tcomp", "tconv", "ttotal"]:
        height = data[method][version][mode][size][proc][run][tname]

        plt.bar(
            np.arange(len(xticks)),
            height=height,
            width=0.1,
            label=tname,
            zorder=2,
            color=color["time"][tname]
        )

# Speedup, Noconv, size=all, proc=all
for size in [2048, 4096, 6144]:
    # for method in ["jacobi", "gauss", "redblack"]:
    [figw, figh] = plt.rcParams["figure.figsize"]
    plt.figure(figsize=(figw, figh))
    plt.title("Speedup")
    plt.xlabel("Number of processes")
    plt.ylabel("Speedup")
    plt.xticks(xticks["speedup"], xticklabels["speedup"])

    n = len(methods)
    w = 0.4 / n ** 0.5
    offset = -(n-1) * w/2

    x = [xtick + offset for xtick in xticks[method][0]]

    for method in methods:
        height = [
            data[method]["mpi"]["noconv"][size][p][1]["speedup"]
                for p in proc
        ]

        plt.bar(
            x=x,
            height=height,
            width=w,
            label=method,
            color=color["speedup"][method]
        )

        plt.legend()
        offset += w

    plt.tight_layout(h_pad=5)
    filename = f"../graphs/speedup-{size}.pdf"
    plt.savefig(filename)
    plt.close()


# Time, No conv, size=all, proc=all, total, comp
for size in ["2048", "4096", "6144"]:
    for method in methods:
        [figw, figh] = plt.rcParams["figure.figsize"]
        plt.figure(figsize=(figw, figh))
        plt.title(f"{method}, no convergence, {size}x{size}")
        plt.grid(True, zorder=0)
        plt.xlabel("Method_Processes")
        plt.ylabel("Time (sec)")
        xticks = [f"{method[0]}_{procs}" for method in methods for proc in procs]
        plt.xticks(range(len(xticks)), xticks)

        for tname in ["tcomp", "tconv", "ttotal"]:
            height = data[method][version][mode][size][proc][run][tname]

            plt.bar(
                np.arange(len(xticks)),
                height=height,
                width=0.1,
                label=tname,
                zorder=2,
                color=color["time"][tname]
            )
