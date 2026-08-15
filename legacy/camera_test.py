from picamera2 import Picamera2
import cv2
import time

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (1280, 720), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()

time.sleep(2)

try:
    while True:
        frame = picam2.capture_array()

        cv2.imshow("Camera Module 3", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
