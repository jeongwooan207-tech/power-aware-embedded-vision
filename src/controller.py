def select_camera_mode(cpu_usage, current_mode):
	"""
	Select camera performance mode based on CPU usage using hysteresis to avoid frequent mode switching.
	"""


	if cpu_usage is None:
		return current_mode

	if current_mode == "HIGH":

		if cpu_usage >= 6:
			return "MEDIUM"

		return "HIGH"

	elif current_mode == "MEDIUM":

		if cpu_usage < 3:
			return "HIGH"

		elif cpu_usage >= 9:
			return "LOW"

		return "MEDIUM"

	elif current_mode == "LOW":

		if cpu_usage < 6:
			return "MEDIUM"

		return "LOW"

	return "MEDIUM"
