# Power-Aware Road Hazard Detection System

A real-time road hazard detection system developed using a Raspberry Pi 5,
Camera Module 3, Python, OpenCV and YOLO.

## Project Goal

The goal of this project is to detect road users such as pedestrians,
cars, bicycles and motorcycles and evaluate potential collision risks.

The system will also adjust its processing mode according to the detected
risk level to reduce unnecessary computation.

## Hardware

- Raspberry Pi 5
- Raspberry Pi Camera Module 3
- microSD card
- Raspberry Pi power supply

## Software

- Raspberry Pi OS
- Python
- Picamera2
- OpenCV
- Ultralytics YOLO

## Current Features

- Camera image acquisition
- Real-time object detection
- Bounding box visualization

## Planned Features

- Pedestrain and vehicle detection
- FPS measurement
- CPU temperature monitoring
- Road risk zone detection
- Object approach estimation
- ECO, NORMAL and PERFORMANCE modes
- Performance data logging

## Project Structure

```text
camera_project/
├── src/
│   └── main.py
├── results/
├── docs/
├── images/
├── requirements.txt
├── .gitignore
└── README.md
```

## Run

Activate the Python virtual environment:

```bash
source yolo_env/bin/activate
```

Run the detection program:

```bash
python3 src/main.py
```

Press `q` to close the camera window.

## Development Status

### Version 0.1

- Raspberry Pi Camera Module 3 connection completed
- YOLO object detection completed
- Real-time bounding box display completed
