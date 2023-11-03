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

                    if size != 1024:
                        data[method][version][mode][size][proc][1]["speedup"] = (
                            data[method]["mpi"][mode][size][1][1]["ttotal"] /
                            data[method][version][mode][size][proc][1]["ttotal"]
                        )
# print(data["jacobi"]["mpi"]["conv"][1024])
# print(data["gauss"]["mpi"]["conv"][1024])
# print(data["redblack"]["mpi"]["conv"][1024])
# Jacobi darkgoldenrod goldenrod gold
# Gauss royalblue cornflowerblue lightblue
# RedBlack firebrick tomato lightsalmon

configs = {
    "speedup-noconv": {
        "sizes": [2048, 4096, 6144],
        "title": "Speedup w/o convergence test",
        "xlabel": "#procs",
        "ylabel": "Speedup",
        "xticks": ["1", "2", "4", "8", "16", "32", "64"],
        "procs": [1, 2, 4, 8, 16, 32, 64],
        "colors": {
            "jacobi": {
                "speedup": "lightgreen"
            },
            "gauss": {
                "speedup": "limegreen"
            },
            "redblack": {
                "speedup": "darkgreen"
            }
        },
        "tnames": ["speedup"]

    },
    "time-noconv": {
        "sizes": [2048, 4096, 6144],
        "title": "Time w/o convergence test",
        "xlabel": "Method.#procs",
        "ylabel": "Time (sec)",
        "xticks": ["8", "16", "32", "64"],
        "procs": [8, 16, 32, 64],
        "colors": {
            "jacobi": {
                "tcomp": "darkgoldenrod",
                "ttotal": "gold"
            },
            "gauss": {
                "tcomp": "royalblue",
                "ttotal": "lightblue"
            },
            "redblack": {
                "tcomp": "firebrick",
                "ttotal": "lightsalmon"
            }
        },
        "tnames": ["ttotal", "tcomp"]
    }
}

methods = ["jacobi", "gauss", "redblack"]

version = "mpi"

for configname, config in configs.items():
    mode = configname.split("-")[1]

    for size in config["sizes"]:
        figw, figh = plt.rcParams["figure.figsize"]
        plt.figure(figsize=(figw, figh))
        plt.title(config["title"])
        plt.grid(True, zorder=0)

        plt.xlabel(config["xlabel"])
        plt.ylabel(config["ylabel"])

        xticks = config["xticks"]

        plt.xticks(range(len(xticks)), xticks)

        width = 0.25 if configname.split("-")[0] == "speedup" else 0.25

        for tname in config["tnames"]:
            # print(configname)

            offsets = [-width, 0, width] if tname == "speedup" else [-width, 0, width]

            for method, offset in zip(methods, offsets):
                # print(method, version, mode)
                # print(data[method][version][mode])
                height = [data[method][version][mode][size][proc][1][tname] for proc in config["procs"]]

                print(np.arange(len(xticks)) + offset)
                print(height)

                print(config["colors"])

                plt.bar(
                    np.arange(len(xticks)) + offset,
                    height=height,
                    width=width,
                    zorder=2,
                    label=f"{method}-{tname}",
                    color=config["colors"][method][tname]
                )

        plt.legend()
        filename = f"../graphs/{configname}-{size}.pdf"
        plt.savefig(filename)
        plt.close()
