import re
import subprocess


def read_pmic_adc():
	"""
	Read Raspberry Pi 5 PMIC ADC measurements.
	"""


	try:
		result = subprocess.run(
			["vcgencmd", "pmic_read_adc"],
			capture_output=True,
			text=True,
			check=True
		)

	except (subprocess.SubprocessError, FileNotFoundError):
		return None

	measurements = {}

	pattern = re.compile(
		r"^\s*([A-Z0-9_]+)\s+"
		r"(?:current|volt)\(\d+\)="
		r"([-+]?[0-9]*\.?[0-9]+)[AV]"
	)

	for line in result.stdout.splitlines():

		match = pattern.match(line)

		if match:
			name = match.group(1)
			value = float(match.group(2))

			measurements[name] = value

	return measurements


def get_core_power():
	"""
	Read VDD_CORE voltage/current and calculate rail power.
	"""

	measurements = read_pmic_adc()

	if measurements is None:
		return None, None, None

	voltage = measurements.get("VDD_CORE_V")
	current = measurements.get("VDD_CORE_A")

	if voltage is None or current is None:
		return None, None, None

	power = voltage * current

	return voltage, current, power


if __name__ == "__main__":

	voltage, current, power = get_core_power()

	if voltage is None:
		print("PMIC measurement failed.")

	else:
		print(f"VDD_CORE Voltage: {voltage:.3f} V")
		print(f"VDD_CORE Current: {current:.3f} A")
		print(f"VDD_CORE Power: {power:.3f} W")
