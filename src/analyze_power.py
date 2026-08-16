import csv
import os
import statistics

import matplotlib.pyplot as plt


LOG_FILE = "data/power_runs_summary.csv"

MODES = ["LOW", "MEDIUM", "HIGH"]


def main():

    # Store measurement results for each camera mode
    results = {
        mode: {
            "temperature": [],
            "cpu_usage": [],
            "load_average": [],
            "fps": [],
            "voltage": [],
            "current": [],
            "power": []
        }
        for mode in MODES
    }

    # Read experiment summary CSV
    with open(LOG_FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            mode = row["camera_mode"]

            if mode not in results:
                continue

            results[mode]["temperature"].append(
                float(row["temperature"])
            )

            results[mode]["cpu_usage"].append(
                float(row["cpu_usage"])
            )

            results[mode]["load_average"].append(
                float(row["load_average"])
            )

            results[mode]["fps"].append(
                float(row["fps"])
            )

            results[mode]["voltage"].append(
                float(row["voltage"])
            )

            results[mode]["current"].append(
                float(row["current"])
            )

            results[mode]["power"].append(
                float(row["power"])
            )

    # Lists for graph data
    avg_powers = []
    power_stds = []

    avg_fps_values = []
    fps_stds = []

    avg_cpu_values = []
    cpu_stds = []

    avg_efficiency_values = []

    print()
    print("Final PMIC Power Analysis")
    print("=========================")

    # Analyze each camera mode
    for mode in MODES:

        data = results[mode]

        if not data["power"]:
            print(f"No data available for {mode}")
            continue

        # Calculate averages
        avg_temperature = statistics.mean(
            data["temperature"]
        )

        avg_cpu = statistics.mean(
            data["cpu_usage"]
        )

        avg_load = statistics.mean(
            data["load_average"]
        )

        avg_fps = statistics.mean(
            data["fps"]
        )

        avg_voltage = statistics.mean(
            data["voltage"]
        )

        avg_current = statistics.mean(
            data["current"]
        )

        avg_power = statistics.mean(
            data["power"]
        )

        # Calculate standard deviations
        temperature_std = statistics.stdev(
            data["temperature"]
        )

        cpu_std = statistics.stdev(
            data["cpu_usage"]
        )

        fps_std = statistics.stdev(
            data["fps"]
        )

        power_std = statistics.stdev(
            data["power"]
        )

        # Performance per VDD_CORE rail power
        performance_per_power = avg_fps / avg_power

        # Store values for graphs
        avg_powers.append(avg_power)
        power_stds.append(power_std)

        avg_fps_values.append(avg_fps)
        fps_stds.append(fps_std)

        avg_cpu_values.append(avg_cpu)
        cpu_stds.append(cpu_std)

        avg_efficiency_values.append(
            performance_per_power
        )

        # Print analysis results
        print()
        print(mode)
        print("-------------------------")

        print(
            f"Temperature        : "
            f"{avg_temperature:.2f} ± "
            f"{temperature_std:.2f} C"
        )

        print(
            f"CPU Usage          : "
            f"{avg_cpu:.2f} ± "
            f"{cpu_std:.2f} %"
        )

        print(
            f"Load Average       : "
            f"{avg_load:.2f}"
        )

        print(
            f"FPS                : "
            f"{avg_fps:.2f} ± "
            f"{fps_std:.2f}"
        )

        print(
            f"Core Voltage       : "
            f"{avg_voltage:.3f} V"
        )

        print(
            f"Core Current       : "
            f"{avg_current:.3f} A"
        )

        print(
            f"Core Power         : "
            f"{avg_power:.3f} ± "
            f"{power_std:.3f} W"
        )

        print(
            f"Performance/Power  : "
            f"{performance_per_power:.2f} FPS/W"
        )

    # Create directory for graphs
    os.makedirs(
        "results",
        exist_ok=True
    )

    # --------------------------------------------------
    # Graph 1: Camera Mode vs VDD_CORE Power
    # --------------------------------------------------

    plt.figure()

    plt.bar(
        MODES,
        avg_powers,
        yerr=power_stds,
        capsize=5
    )

    plt.xlabel("Camera Mode")
    plt.ylabel("VDD_CORE Power (W)")
    plt.title(
        "Camera Mode vs Average Core Power"
    )

    plt.tight_layout()

    plt.savefig(
        "results/core_power.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------
    # Graph 2: Camera Mode vs FPS
    # --------------------------------------------------

    plt.figure()

    plt.bar(
        MODES,
        avg_fps_values,
        yerr=fps_stds,
        capsize=5
    )

    plt.xlabel("Camera Mode")
    plt.ylabel("Camera FPS")
    plt.title(
        "Camera Mode vs Average FPS"
    )

    plt.tight_layout()

    plt.savefig(
        "results/fps.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------
    # Graph 3: Camera Mode vs CPU Usage
    # --------------------------------------------------

    plt.figure()

    plt.bar(
        MODES,
        avg_cpu_values,
        yerr=cpu_stds,
        capsize=5
    )

    plt.xlabel("Camera Mode")
    plt.ylabel("CPU Usage (%)")
    plt.title(
        "Camera Mode vs Average CPU Usage"
    )

    plt.tight_layout()

    plt.savefig(
        "results/cpu_usage.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------
    # Graph 4: Performance per Power
    # --------------------------------------------------

    plt.figure()

    plt.bar(
        MODES,
        avg_efficiency_values
    )

    plt.xlabel("Camera Mode")
    plt.ylabel(
        "Performance / Power (FPS/W)"
    )

    plt.title(
        "Camera Performance per VDD_CORE Power"
    )

    plt.tight_layout()

    plt.savefig(
        "results/performance_per_power.png",
        dpi=300
    )

    plt.close()

    print()
    print("=========================")
    print("Analysis completed.")
    print("Graphs saved to: results/")


if __name__ == "__main__":
    main()
