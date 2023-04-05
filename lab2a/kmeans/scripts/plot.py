#!/usr/bin/env python

import sys
import glob
import collections
import matplotlib.pyplot as plt
import numpy as np

results = collections.defaultdict(lambda: collections.defaultdict(list))

for filename in sorted(glob.glob("../outputs/*")):
	instance = "".join(filter(lambda x: not x.isdigit(), filename))[11:-5]
	threadsString = "".join(filter(lambda x: x.isdigit(), filename))

	if threadsString == "":
		continue

	threads = int(threadsString)

	with open(filename) as f:
		lines = f.readlines()

		for line in lines:
			line = line.strip()
			if line.startswith("nloops"):
				time = float(line.split()[5][:-2])

		results[instance]["time"].append(time)

sequential_easy = results["sequential-easy"]["time"][0]
sequential_hard = results["sequential-hard"]["time"][0]

for instance, measurements in results.items():
	times = measurements["time"]
	for time in times:
		if (instance == "naive-aff"
			or instance == "naive-no-aff"
			or instance == "reduction-easy"
			or instance == "reduction-numa-easy"
			or instance == "sequential-easy"):
			sequential = sequential_easy
		else:
			sequential = sequential_hard
		measurements["speedup"].append(sequential / time)

def print_dict(d):
	for instance, measurements in d.items():
		print(instance)
		for type, values in measurements.items():
			print(f"type={type}, values={values}")
		print()

print_dict(results)

setups = [
	{
		"names": ["naive-no-aff"],
		"title": "K-means: Naive",
		"labels": ["Naive"]
	},
	{
		"names": ["naive-no-aff", "naive-aff"],
		"title": "K-means: Naive (GOMP_CPU_AFFINITY)",
		"labels": ["w/o GOMP_CPU_AFFINITY", "w/ GOMP_CPU_AFFINITY"]
	},
	# We take COMP_CPU_AFFINITY for granted from now on
	{
		"names": ["naive-aff", "reduction-easy"],
		"title": "K-means: Naive vs. Reduction",
		"labels": ["Naive", "Reduction"]
	},
	{
		"names": ["reduction-easy", "reduction-hard-no-fs"],
		"title": "K-means: Reduction",
		"labels": ["Coords: 16, Clusters: 16", "Coords: 1, Clusters: 4"]
	},
	{
		"names": ["reduction-hard-no-fs", "reduction-hard-fs"],
		"title": "K-means: Reduction (first-touch)",
		"labels": ["Not utilizing first-touch", "Utilizing first-touch"]
	},
	{
		"names": ["reduction-hard-fs", "reduction-numa-hard"],
		"title": "K-means: NUMA, Coords: 1, Clusters: 4",
		"labels": ["Non NUMA-aware", "NUMA-aware"]
	},
	{
		"names": ["reduction-easy", "reduction-numa-easy"],
		"title": "K-means: NUMA, Coords: 16, Clusters: 16",
		"labels": ["Non NUMA-aware", "NUMA-aware"]
	}
]

for setup in setups:

	for time in [True, False]:
		plt.title(f"{setup['title']}, {'Time' if time else 'Speedup'}")
		plt.grid(True, zorder=0)

		plt.xlabel("Threads")
		plt.ylabel("Time (sec)" if time else "Speedup")

		xticks = ["seq", "1", "2", "4", "8", "16", "32", "64"]
		plt.xticks(range(len(xticks)), xticks)

		w = 0.4
		n = len(setup["names"])
		offset = -(n-1) * w/2

		for k, requested in enumerate(setup["names"]):
			resource = "time" if time else "speedup"

			if (requested == "naive-aff"
				or requested == "naive-no-aff"
				or requested == "reduction-easy"
				or requested == "reduction-numa-easy"):
					string_sequential = "sequential-easy"
			else:
				string_sequential = "sequential-hard"

			sequential = results[string_sequential][resource]
			print(f"requested={requested} sequential={string_sequential}")
			threads = results[requested][resource]
			concat = sequential + threads

			color = {
				"time": ["tab:blue", "tab:orange"],
				"speedup": ["tab:green", "tab:red"]
			}[resource][k]

			plt.bar(
				np.arange(len(xticks)) + offset,
				height=concat,
				width=w,
				label=setup["labels"][k],
				zorder=2,
				color=color
			)

			offset += w

		plt.legend()
		filename = f"../graphs/{'_'.join(setup['names'])}-{resource}.pdf"
		plt.savefig(filename)
		plt.close()
