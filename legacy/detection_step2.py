from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import time
from datetime import datetime

model = YOLO("yolo11n.pt")

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()

time.sleep(2)

# 표시할 물체
target_objects = {
    "person",
    "bottle",
    "cup",
    "cell phone"
}

previous_time = time.time()

try:
    while True:
        frame = picam2.capture_array()

        results = model.predict(
            source=frame,
            imgsz=320,
            conf=0.5,
            verbose=False
        )

        result = results[0]

        # FPS 계산
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        detected_objects = []

        # 인식 결과를 하나씩 확인
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            object_name = model.names[class_id]

            if object_name not in target_objects:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detected_objects.append(object_name)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = f"{object_name} {confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        cv2.imshow("Object Detection Step 2", frame)

        key = cv2.waitKey(1) & 0xFF

        # q: 종료
        if key == ord("q"):
            break

        # s: 현재 화면 저장
        if key == ord("s"):
            filename = datetime.now().strftime(
                "detected_%Y%m%d_%H%M%S.jpg"
            )

            cv2.imwrite(filename, frame)
            print(f"사진 저장 완료: {filename}")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
