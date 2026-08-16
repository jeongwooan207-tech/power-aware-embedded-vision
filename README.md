# Power-Aware Embedded Vision System

A Raspberry Pi 5 based embedded system for workload monitoring, adaptive camera control, power monitoring, and thermal management.

The Raspberry Pi Camera Module 3 is used as a configurable workload. The system monitors CPU load, temperature, system load, and camera performance, logs the measurements, and dynamically adjusts the camera operating mode.

The final goal is to balance:

**Performance ↔ Power ↔ Temperature**

using a power-aware embedded controller.

---

## Current Features

* CPU temperature monitoring
* CPU usage monitoring
* system load monitoring
* camera FPS measurement
* Raspberry Pi Camera Module 3 integration
* LOW / MEDIUM / HIGH camera modes
* adaptive camera mode control
* live camera preview
* real-time camera mode, FPS, and CPU temperature overlay
* CSV data logging

### Camera Modes

```text
LOW
640 x 480
10 FPS

MEDIUM
1280 x 720
20 FPS

HIGH
1920 x 1080
30 FPS
```

The different modes create different computational workloads on the Raspberry Pi 5.

The live preview window keeps a fixed display size while the camera resolution and target FPS change according to the selected operating mode.

---

## Hardware

* Raspberry Pi 5
* Raspberry Pi Camera Module 3
* Raspberry Pi 5 compatible cooling fan
* Raspberry Pi power supply
* microSD card

The cooling fan is connected to the dedicated Raspberry Pi 5 fan connector and will later be used for active thermal management.

---

## Project Structure

```text
src/
|
|-- main.py
|   `-- Overall system orchestration and live camera display
|
|-- monitor.py
|   |-- CPU temperature
|   |-- CPU usage
|   `-- System load
|
|-- camera.py
|   |-- Camera configuration
|   |-- Resolution control
|   |-- FPS control
|   `-- Frame capture
|
|-- controller.py
|   `-- Adaptive camera mode control
|
`-- logger.py
    `-- CSV data logging
```

---

## Development Roadmap

### Stage 1 - Camera Workload [Completed]

* Camera Module 3 integration
* frame capture
* resolution control
* FPS control

### Stage 2 - Monitoring and Logging [Completed]

* CPU temperature
* CPU usage
* system load
* camera FPS
* CSV logging

### Stage 3 - Power-Aware Controller [Completed]

* LOW / MEDIUM / HIGH camera modes
* dynamic camera mode selection
* workload-based camera control
* live camera preview
* real-time camera mode, FPS, and CPU temperature display
* fixed-size preview window independent of camera operating mode

### Stage 4 - PMIC Power Monitoring [Planned]

The Raspberry Pi 5 PMIC provides internal voltage and current measurements.

Power can be calculated using:

**P = V x I**

Planned features:

* voltage monitoring
* current monitoring
* CPU core power calculation
* PMIC rail power estimation
* power data logging
* comparison of power consumption between camera modes

### Stage 5 - Thermal Management [Planned]

The existing Raspberry Pi 5 fan will be integrated into the controller.

Planned features:

* temperature-dependent fan control
* fan speed control
* coordination between camera workload and cooling
* power-aware thermal management

---

## System Concept

```text
CPU Temperature
CPU Usage
System Load
Camera FPS
PMIC Power
      |
      v
Power / Thermal Controller
      |
  +---+---+
  |       |
  v       v
Camera   Fan
Mode     Control
```

The final controller will dynamically manage system performance, power consumption, and temperature.

---

## Current Status

**Stage 3 completed**

Current system:

```text
Camera Workload
      |
      v
System Monitoring
      |
      +----> Live Camera Preview
      |       Mode / FPS / CPU Temp
      |
      v
CSV Logging
      |
      v
Power-Aware Camera Controller
```

Next step:

```text
Stage 4
PMIC Voltage / Current / Power Monitoring
```

---

## Future Extensions

* external voltage/current sensor integration
* more accurate total input power measurement
* advanced fan control
* thermal hysteresis
* power-budget-based workload control
* power-performance optimization
