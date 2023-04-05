#!/usr/bin/env python

import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# matplotlib.use('Agg')

# A dictionary in the form of:
# {
# 	board_size: [(threads, time), (threads, time), ...]
#   board_size: [(threads, time), (threads, time), ...]
#   ...
# }
xy = {}

with open("run_Game_Of_Life.out") as f:
	for line in f.readlines():
		tokens = line.split(" ")

		if (line.startswith("Using")):
			threads = int(tokens[1])

		elif (line.startswith("GameOfLife")):
			size = int(tokens[2])
			time = float(tokens[6])

			if size not in xy:
				xy[size] = []

			xy[size].append((threads, time))

for size in xy:
	print(f"Time, {size}x{size}: {xy[size]}")

	(threads_axis, time_axis) = zip(*xy[size])

	fig, ax = plt.subplots()
	plt.title(f"{size}x{size}, Time")
	ax.grid(True)
	ax.set_xlabel("Threads")
	ax.set_ylabel("Time (sec)")
	ax.xaxis.set_ticks(threads_axis)

	ax.plot(threads_axis, time_axis, color="red", marker='x')

	plt.savefig(f"time-{size}.pdf", bbox_inches="tight")

for size in xy:
	print(f"Speedup, {size}x{size}: {xy[size]}")

	(threads_axis, time_axis) = zip(*xy[size])

	baseline = time_axis[0]

	speedup_axis = [baseline / item for item in time_axis]

	fig, ax = plt.subplots()
	plt.title(f"{size}x{size}, Speedup")
	ax.grid(True)
	ax.set_xlabel("Threads")
	ax.set_ylabel("Speedup")
	ax.xaxis.set_ticks(threads_axis)

	ax.plot(threads_axis, speedup_axis, color="green", marker='x')

	plt.savefig(f"speedup-{size}.pdf", bbox_inches="tight")

plt.show()
