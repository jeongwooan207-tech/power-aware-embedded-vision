import time
import cv2

from monitor import get_cpu_temperature, get_load_average, get_cpu_usage

from camera import start_camera, change_camera_mode, capture_frame, stop_camera

from controller import select_camera_mode

from logger import initialize_log, log_data

from power import get_core_power

CAMERA_MODE = "HIGH"


def main():

	print("Power-Aware Embedded Vision")
	print("---------------------------")

	log_file = "data/system_log.csv"
	initialize_log(log_file)

	camera = start_camera(CAMERA_MODE)

	current_mode = CAMERA_MODE

	print(f"Camera started: {CAMERA_MODE.upper()} mode")

	frame_count = 0
	last_measurement = time.monotonic()

	actual_fps = 0.0
	temp_text = "N/A"
	temp_display = "N/A"

	core_voltage = None
	core_durrent = None
	core_power = None
	power_text = "N/A"

	last_mode_change = time.monotonic()
	MIN_MODE_DURATION = 5.0


	cv2.namedWindow(
		"Power-Aware Embedded Vision",
		cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO
	)

	cv2.resizeWindow(
		"Power-Aware Embedded Vision",
		960,
		540
	)

	try:

		while True:

			# Capture one camera frame
			frame = capture_frame(camera)

			frame_count += 1

			current_time = time.monotonic()
			elapsed = current_time - last_measurement

			# Print system information once per second
			if elapsed >= 1.0:

				temperature = get_cpu_temperature()
				cpu_usage = get_cpu_usage()
				load = get_load_average()

				core_voltage, core_current, core_power = get_core_power()

				mode = select_camera_mode(cpu_usage, current_mode)


				if (
					mode != current_mode
					and current_time - last_mode_change >= MIN_MODE_DURATION
				):
					change_camera_mode(camera, mode)
					current_mode = mode
					last_mode_change = time.monotonic()

					frame_count = 0
					last_measurement = time.monotonic()

					continue

				actual_fps = frame_count / elapsed


				if temperature is not None:
					temp_text = f"{temperature:.1f} °C"
					temp_display = f"{temperature:.1f} C"
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

				if core_power is not None:
					power_text = f"{core_power:.2f} W"
				else:
					power_text = "N/A"


				print(
					f"CPU Temperature: {temp_text} | "
					f"CPU Usage: {cpu_usage_text} | "
					f"System Load: {load_text} | "
					f"Camera Mode: {current_mode.upper()} | "
					f"Camera FPS: {actual_fps:.1f} | "
					f"VDD_CORE Power: {power_text}"
				)

				log_data(
					log_file,
					current_mode,
					temperature,
					cpu_usage,
					load,
					actual_fps,
					core_voltage,
					core_current,
					core_power
				)

				frame_count = 0
				last_measurement = time.monotonic()


			# Display camera information on frame
			cv2.putText(
				frame,
				f"Mode: {current_mode.upper()}",
				(20, 40),
				cv2.FONT_HERSHEY_SIMPLEX,
				1,
				(0, 255, 0),
				2
			)

			cv2.putText(
				frame,
				f"FPS: {actual_fps:.1f}",
				(20, 80),
				cv2.FONT_HERSHEY_SIMPLEX,
				1,
				(0, 255, 0),
				2
			)

			cv2.putText(
				frame,
				f"CPU Temp: {temp_display}",
				(20, 120),
				cv2.FONT_HERSHEY_SIMPLEX,
				1,
				(0, 255, 0),
				2
			)

			cv2.putText(
				frame,
				f"Power: {power_text}",
				(20, 160),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.7,
				(0, 255, 0),
				2
			)


			# Show live camera window
			cv2.imshow(
				"Power-Aware Embedded Vision",
				frame
			)

			# Press Q to stop the program
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break



	except KeyboardInterrupt:

		print("\nMonitoring stopped.")

	finally:

		stop_camera(camera)
		cv2.destroyAllWindows()

		print("Camera stopped.")

if __name__ == "__main__":
	main()
