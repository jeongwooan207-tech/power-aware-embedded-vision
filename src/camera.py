import time

from picamera2 import Picamera2


CAMERA_MODES = {
    "LOW": {
        "width": 640,
        "height": 480,
        "fps": 5
    },
    "MEDIUM": {
        "width": 1280,
        "height": 720,
        "fps": 15
    },
    "HIGH": {
        "width": 1920,
        "height": 1080,
        "fps": 30
    }
}


def start_camera(mode="MEDIUM"):
    """
    Start Raspberry Pi camera using a predefined camera mode.
    """

    settings = CAMERA_MODES[mode]

    width = settings["width"]
    height = settings["height"]
    fps = settings["fps"]

    camera = Picamera2()

    config = camera.create_video_configuration(
        main={
            "size": (width, height),
            "format": "RGB888"
        },
        controls={
            "FrameRate": fps
        }
    )

    camera.configure(config)
    camera.start()

    time.sleep(1)

    return camera


def change_camera_mode(camera, mode):
	"""
	Change camera resolution and FPS according to the selected mode.
	"""

	settings = CAMERA_MODES[mode]

	width = settings["width"]
	height = settings["height"]
	fps = settings["fps"]

	camera.stop()

	config = camera.create_video_configuration(
		main={
			"size": (width, height),
			"format": "RGB888"
		},
		controls={
			"FrameRate": fps
		}
	)

	camera.configure(config)
	camera.start()



def capture_frame(camera):
    """
    Capture one frame from the camera.
    """

    return camera.capture_array()


def stop_camera(camera):
    """
    Stop and close the camera.
    """

    camera.stop()
    camera.close()
