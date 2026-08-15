import os

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
