import time

from datetime import datetime
from camera import start_camera, capture_frame, stop_camera
from monitor import get_cpu_temperature, get_cpu_usage, get_load_average
from power import get_core_power
from logger import initialize_log, log_data


TEST_DURATION = 60

MODES = ["LOW", "MEDIUM", "HIGH"]


def test_mode(mode_name, log_file):
    """
    Test one camera mode for a fixed duration.
    """

    print()
    print(f"Starting {mode_name} mode test")
    print("---------------------------")

    camera = start_camera(mode_name)

    print("Camera warm-up...")
    time.sleep(5)

    frame_count = 0
    last_measurement = time.monotonic()
    test_start = time.monotonic()

    try:

        while True:

            frame = capture_frame(camera)

            frame_count += 1

            current_time = time.monotonic()

            elapsed = current_time - last_measurement
            total_elapsed = current_time - test_start

            # Stop test after TEST_DURATION seconds
            if total_elapsed >= TEST_DURATION:
                break

            # Measure once per second
            if elapsed >= 1.0:

                temperature = get_cpu_temperature()
                cpu_usage = get_cpu_usage()
                load = get_load_average()

                core_voltage, core_current, core_power = get_core_power()

                actual_fps = frame_count / elapsed

                print(
                    f"Mode: {mode_name} | "
                    f"Time: {total_elapsed:.0f}/{TEST_DURATION}s | "
                    f"Temp: {temperature:.1f} C | "
                    f"CPU: {cpu_usage:.1f} % | "
                    f"FPS: {actual_fps:.2f} | "
                    f"Power: {core_power:.3f} W"
                )

                log_data(
                    log_file,
                    mode_name,
                    temperature,
                    cpu_usage,
                    load,
                    actual_fps,
                    core_voltage,
                    core_current,
                    core_power
                )

                frame_count = 0
                last_measurement = current_time

    finally:

        stop_camera(camera)

    print(f"{mode_name} test completed.")


def main():

    print("PMIC Power Comparison Test")
    print("==========================")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file = f"data/power_test_{timestamp}.csv"


    initialize_log(log_file)

    for mode_name in MODES:

        test_mode(
            mode_name,
            log_file
        )

        # Short pause between modes
        time.sleep(5)

    print()
    print("All tests completed.")
    print(f"Results saved to: {log_file}")


if __name__ == "__main__":
    main()

