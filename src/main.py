import time

from monitor import get_cpu_temperature, get_load_average, get_cpu_usage


def main():

	print("Power-Aware Embedded Vision")
	print("---------------------------")

	try:

		while True:

			temperature = get_cpu_temperature()
			load = get_load_average()
			cpu_usage = get_cpu_usage()

			if temperature is not None:
				temp_text = f"{temperature:.1f} °C"
			else:
				temp_text = "N/A"

			if load is not None:
				load_text = f"{load:.2f}"
			else:
				load_text = "N/A"

			if cpu_usage is not None:
				cpu_usage_text = f"{cpu_usage:.1f} %"
			else:
				cpu_usage_text = "N/A"


			print(
				f"CPU Temperature: {temp_text} | "
				f"CPU Usage: {cpu_usage_text} | "
				f"System Load: {load_text}"
			)

			time.sleep(1)

	except KeyboardInterrupt:

			print("\nMonitoring stopped.")

if __name__ == "__main__":
	main()
