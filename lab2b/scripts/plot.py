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

sequential = results["kmeans_seq"]["time"]

def print_dict(d):
	for instance, measurements in d.items():
		print(instance)
		for type, values in measurements.items():
			print(f"type={type}, values={values}")
		print()

print_dict(results)

setups = [
	{
		"names": [
			"kmeans_omp_array_lock",
			"kmeans_omp_clh_lock",
			"kmeans_omp_critical",
			"kmeans_omp_naive",
			"kmeans_omp_nosync_lock",
			"kmeans_omp_pthread_mutex_lock",
			"kmeans_omp_pthread_spin_lock",
			"kmeans_omp_tas_lock",
			"kmeans_omp_ttas_lock"
		],
		"title": "All mutual exclusion implementations, threads 1-64",
		"labels": [
			"array_lock",
			"clh_lock",
			"critical",
			"naive",
			"nosync_lock",
			"pthread_mutex_lock",
			"pthread_spin_lock",
			"tas_lock",
			"ttas_lock"
		],
		"filename": "all-locks",
		"threads": ["1", "2", "4", "8", "16", "32", "64"]
	},
	{
		"names": [
			"kmeans_omp_array_lock",
			"kmeans_omp_clh_lock",
			"kmeans_omp_critical",
			"kmeans_omp_naive",
			"kmeans_omp_nosync_lock",
			"kmeans_omp_pthread_mutex_lock",
			"kmeans_omp_pthread_spin_lock",
			"kmeans_omp_tas_lock",
			"kmeans_omp_ttas_lock"
		],
		"title": "All mutual exclusion implementations, threads 1-16",
		"labels": [
			"array_lock",
			"clh_lock",
			"critical",
			"naive",
			"nosync_lock",
			"pthread_mutex_lock",
			"pthread_spin_lock",
			"tas_lock",
			"ttas_lock"
		],
		"filename": "all-locks-16",
		"threads": ["1", "2", "4", "8", "16"]
	},
	# {
	# 	"names": [
	# 		"kmeans_omp_array_lock",
	# 		"kmeans_omp_clh_lock",
	# 		"kmeans_omp_naive",
	# 		"kmeans_omp_nosync_lock",
	# 		"kmeans_omp_pthread_mutex_lock",
	# 		"kmeans_omp_pthread_spin_lock",
	# 		"kmeans_omp_ttas_lock"
	# 	],
	# 	"title": "Ignoring omp_critical and tas_lock",
	# 	"labels": [
	# 		"array_lock",
	# 		"clh_lock",
	# 		"naive",
	# 		"nosync_lock",
	# 		"pthread_mutex_lock",
	# 		"pthread_spin_lock",
	# 		"ttas_lock"
	# 	],
	# 	"filename": "no-critical-no-tas"
	# },
	# {
	# 	"names": [
	# 		"kmeans_omp_array_lock",
	# 		"kmeans_omp_clh_lock",
	# 		"kmeans_omp_naive",
	# 		"kmeans_omp_nosync_lock",
	# 	],
	# 	"title": "Ignoring pthread_spin_lock, pthread_mutex_lock and ttas_lock",
	# 	"labels": [
	# 		"array_lock",
	# 		"clh_lock",
	# 		"naive",
	# 		"nosync_lock",
	# 	],
	# 	"filename": "no-spinlock-no-mutex-no-ttas"
	# },
	# {
	# 	"names": [
	# 		"kmeans_omp_clh_lock",
	# 		"kmeans_omp_naive",
	# 		"kmeans_omp_nosync_lock",
	# 	],
	# 	"title": "Ignoring array_lock",
	# 	"labels": [
	# 		"clh_lock",
	# 		"naive",
	# 		"nosync_lock",
	# 	],
	# 	"filename": "no-array"
	# },
]

for setup in setups:
	[figw, figh] = plt.rcParams["figure.figsize"]

	plt.figure(figsize=(figw, figh))

	plt.title(f"{setup['title']}")
	plt.grid(True, zorder=0)

	plt.xlabel("Threads")
	plt.ylabel("Time (sec)")

	xticks = setup["threads"]
	plt.xticks(range(len(xticks)), xticks)

	w = 0.8 / len(setup["names"])
	n = len(setup["names"])
	offset = -(n-1) * w/2

	for k, requested in enumerate(setup["names"]):
		resource = "time"

		sequential = results["kmeans_seq"][resource]
		threads = results[requested][resource][0:len(setup["threads"])]
		# concat = sequential + threads
		concat = threads

		color = {
			"time": [
				"tab:blue",
				"tab:orange",
				"tab:green",
				"tab:red",
				"tab:purple",
				"tab:brown",
				"tab:pink",
				"tab:gray",
				"tab:olive",
				"tab:cyan",
			],
			"speedup": ["tab:green", "tab:red"]
		}[resource][k]

		plt.axhline(y=sequential, linewidth=8*w, color="tab:red", zorder=0)
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
	filename = f"../graphs/{setup['filename']}.pdf"
	plt.savefig(filename)
	plt.close()
