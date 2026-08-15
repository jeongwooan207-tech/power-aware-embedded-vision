import os
import time

def get_cpu_temperature():
	"""
	Read Raspberry Pi CPU temperature in degrees Celsius.
	"""

	path = "/sys/class/thermal/thermal_zone0/temp"

	try:
		with open(path, "r") as file:
			temp_raw = file.read().strip()

		return float(temp_raw) / 1000.0

	except (FileNotFoundError, ValueError):
		return None


def get_load_average():
	"""
	Return the 1-minute system load average.
	"""

	try:
		return os.getloadavg()[0]

	except OSError:
		return None


def read_cpu_times():
	"""
	Read CPU time values from /proc/stat.
	"""

	try:
		with open("/proc/stat", "r") as file:
			line = file.readline()

		values = line.split()[1:]
		values = [int(value) for value in values]

		idle = values[3]
		total = sum(values)

		return idle, total

	except (OSError, ValueError, IndexError):
		return None


def get_cpu_usage(interval=0.1):
	"""
	Calculate CPU usage in percent.
	"""

	first = read_cpu_times()

	if first is None:
		return None

	time.sleep(interval)

	second = read_cpu_times()

	if second is None:
		return None

	idle_1, total_1 = first
	idle_2, total_2 = second

	idle_delta = idle_2 - idle_1
	total_delta = total_2 - total_1

	if total_delta == 0:
		return 0.0

	usage = 100.0 * (1.0 - idle_delta / total_delta)

	return usage

