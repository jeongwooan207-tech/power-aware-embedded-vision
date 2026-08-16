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
				"fps",
				"core_voltage",
				"core_current",
				"core_power"
			])


def log_data(
	log_file,
	current_mode,
	temperature,
	cpu_usage,
	load,
	actual_fps,
	core_voltage,
	core_current,
	core_power
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
			round(temperature, 2),
			round(cpu_usage, 2),
			round(load, 2),
			round(actual_fps, 2),
			round(core_voltage, 3) if core_voltage is not None else None,
			round(core_current, 3) if core_current is not None else None,
			round(core_power, 3) if core_power is not None else None
		])
