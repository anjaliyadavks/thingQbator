'''
import cv2
from yolo_detector import YoloDetector
from tts_output import speak
from utils import classify_traffic_light_color, draw_box, Debouncer
from config import CAMERA_INDEX, SPEECH_COOLDOWN

VEHICLE_CLASSES = {"car", "bus", "truck", "motorcycle", "bicycle"}

def main():
    det = YoloDetector()
    deb = Debouncer(cooldown=SPEECH_COOLDOWN)

    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(3, 640)
    cap.set(4, 480)

    if not cap.isOpened():
        print("❌ Camera failed to open")
        return

    print("✅ BlindAssist running... Press 'q' to quit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = det.detect(frame)
        vehicle_present = False

        for d in detections:
            name = d["name"]
            xy = d["xyxy"]

            # =========================
            # 🚦 TRAFFIC LIGHT LOGIC
            # =========================
            if name == "traffic light":
                color = classify_traffic_light_color(frame, xy)
                draw_box(frame, xy, f"{color}")

                if color == "red" and deb.can_speak("red"):
                    speak("Red light. Please wait.")

                elif color == "green" and deb.can_speak("green"):
                    speak("Green light. You can cross now.")

                elif color in ("yellow", "orange") and deb.can_speak("yellow"):
                    speak("Yellow light. Be careful.")

            # =========================
            # 🚗 VEHICLE WARNING LOGIC
            # =========================
            elif name in VEHICLE_CLASSES:
                vehicle_present = True
                draw_box(frame, xy, name)

        # Speak vehicle warning only once every few seconds
        if vehicle_present and deb.can_speak("vehicle"):
            speak("Vehicle approaching. Do not cross.")

        cv2.imshow("BlindAssist", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
'''
# yolo_detector.py
from ultralytics import YOLO

class YoloDetector:
    def __init__(self):
        print("📌 Loading YOLOv8n.pt model...")
        self.model = YOLO("yolov8n.pt")
        self.names = self.model.model.names

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]
        detections = []

        # Only detect things required for blind assistance
        ALLOWED = ["person", "traffic light", "car", "bus", "truck", "motorcycle", "bicycle"]

        for box in results.boxes:
            cls = int(box.cls[0])
            name = self.names[cls]

            # Skip unwanted objects
            if name not in ALLOWED:
                continue

            conf = float(box.conf[0])
            xyxy = [int(x) for x in box.xyxy[0].tolist()]

            detections.append({
                "name": name,
                "conf": conf,
                "xyxy": xyxy
            })

        return detections

