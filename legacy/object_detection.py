from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import time

model = YOLO("yolo11n.pt")

picam2 = Picamera2()

config = picam2.create_preview_configuration(
	main={"size": (640, 480), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()

time.sleep(2)

try:
    while True:
        
        frame = picam2.capture_array()

        
        results = model.predict(
            source=frame,
            imgsz=320,
            conf=0.5,
            verbose=False
        )

        
        detected_frame = results[0].plot()

        cv2.imshow("YOLO Object Detection", detected_frame)

        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()

