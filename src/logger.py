import csv
import os
from datetime import datetime


def initialize_log(filepath):
	"""
	Create CSV log file and write the header if the file does not exist.
	"""

	if not os.path.exists(filepath):

		with open(filepath, "w", newline="") as file:

			writer = csv.writer(file)

			writer.writerow([
				"timestamp",
				"camera_mode",
				"cpu_temperature",
				"cpu_usage",
				"load_average",
				"fps"
			])


def log_data(
	log_file,
	current_mode,
	temperature,
	cpu_usage,
	load,
	actual_fps
):
	"""
	Append ne measurement to the CSV log file.
	"""

	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	with open(log_file, "a", newline="") as file:

		writer = csv.writer(file)

		writer.writerow([
			timestamp,
			current_mode,
			temperature,
			cpu_usage,
			load,
			actual_fps
		])

