# main.py
'''
import cv2
from yolo_detector import YoloDetector
#from face_recognizer import FaceRecognizer
from tts_output import speak
from utils import classify_traffic_light_color, draw_box, Debouncer
from config import CAMERA_INDEX, SPEECH_COOLDOWN

VEHICLE_CLASSES = set(['car','truck','bus','motorcycle','bicycle'])

def main():
    det = YoloDetector()
    fr =None
    deb = Debouncer(cooldown=SPEECH_COOLDOWN)
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(3,640); cap.set(4,480)
    if not cap.isOpened():
        print('Failed to open camera'); return
    while True:
        ret, frame = cap.read()
        if not ret: break
        detections = det.detect(frame)
        vehicle_present = False
        for d in detections:
            name = d['name']; xy = d['xyxy']
            if name == 'traffic light':
                color = classify_traffic_light_color(frame, xy)
                if color:
                    draw_box(frame, xy, f'TL:{color}')
                    if color == 'red' and deb.can_speak('red_light'): speak('Red light. Please wait.')
                    elif color == 'green' and deb.can_speak('green_light'): speak('Green light. You can cross now.')
                    elif color == 'yellow' and deb.can_speak('yellow_light'): speak('Yellow light. Please be careful.')
            elif name in VEHICLE_CLASSES:
                vehicle_present = True; draw_box(frame, xy, name)
        if vehicle_present and deb.can_speak('vehicle'): speak('Vehicle approaching. Do not cross.')
        for d in detections:
    name = d["name"]
    xy = d["xyxy"]

    # 🚦 TRAFFIC LIGHT DETECTED
    if name == "traffic light":
        color = classify_traffic_light_color(frame, xy)
        draw_box(frame, xy, f"TL:{color}")

        if color == "red" and deb.can_speak("red"):
            speak("Red light ahead. Please wait.")

        elif color == "green" and deb.can_speak("green"):
            speak("Green light. You can cross now.")

        elif color == "yellow" and deb.can_speak("yellow"):
            speak("Yellow light. Be careful.")

    # 🚗 VEHICLE DETECTED
    elif name in VEHICLE_CLASSES:
        vehicle_present = True
        draw_box(frame, xy, name)
	if vehicle_present and deb.can_speak("vehicle"):
	    speak("Vehicle approaching. Do not cross.")


               # if name and deb.can_speak(f'person_{name}'): draw_box(frame,(fx1,fy1,fx2,fy2),name); speak(f'{name} is near you.')
        cv2.imshow('BlindAssist', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release(); cv2.destroyAllWindows()

if __name__ == '__main__': main()

# main.py
import cv2
from yolo_detector import YoloDetector
from tts_output import speak
from utils import classify_traffic_light_color, draw_box, Debouncer
from config import CAMERA_INDEX, SPEECH_COOLDOWN

# Vehicles defined by YOLO model classes
VEHICLE_CLASSES = set(['car', 'truck', 'bus', 'motorcycle', 'bicycle'])


def main():
    # Initialize YOLO detector
    det = YoloDetector()

    # Debouncer = prevents repeating the same voice many times
    deb = Debouncer(cooldown=SPEECH_COOLDOWN)

    # Open webcam
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(3, 640)
    cap.set(4, 480)

    if not cap.isOpened():
        print("❌ Camera could not open")
        return

    print("✅ BlindAssist running... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect objects
        detections = det.detect(frame)

        vehicle_present = False  # Reset for each frame

        # -------------------------
        # PROCESS DETECTIONS
        # -------------------------
        for d in detections:
            name = d["name"]
            xy = d["xyxy"]

            # 🚦 TRAFFIC LIGHT DETECTED
            if name == "traffic light":
                color = classify_traffic_light_color(frame, xy)
                draw_box(frame, xy, f"TL: {color}")

                if color == "red" and deb.can_speak("red"):
                    speak("Red light ahead. Please wait.")

                elif color == "green" and deb.can_speak("green"):
                    speak("Green light. You can cross now.")

                elif color == "yellow" and deb.can_speak("yellow"):
                    speak("Yellow light. Be careful.")

            # 🚗 VEHICLE DETECTED
            elif name in VEHICLE_CLASSES:
                vehicle_present = True
                draw_box(frame, xy, name)

        # If any vehicle detected
        if vehicle_present and deb.can_speak("vehicle"):
            speak("Vehicle approaching. Do not cross.")

        # Show camera output
        cv2.imshow("BlindAssist", frame)

        # Quit on keypress 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

'''
import cv2
from yolo_detector import YoloDetector
from tts_output import speak
from utils import classify_traffic_light_color, draw_box, Debouncer
from config import CAMERA_INDEX, SPEECH_COOLDOWN

VEHICLE_CLASSES = set(['car', 'truck', 'bus', 'motorcycle', 'bicycle'])

def main():
    det = YoloDetector()
    deb = Debouncer(cooldown=SPEECH_COOLDOWN)

    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(3, 640)
    cap.set(4, 480)

    if not cap.isOpened():
        print("❌ Camera could not open!")
        return

    print("✅ BlindAssist running... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame")
            break

        # --- DETECTION ---
        detections = det.detect(frame)
        print("DETECTIONS:", detections)   # DEBUG PRINT

        vehicle_present = False

        for d in detections:
            name = d["name"]
            xy = d["xyxy"]

            # 🚦 TRAFFIC LIGHT
            if name == "traffic light":
                color = classify_traffic_light_color(frame, xy)
                draw_box(frame, xy, f"TL: {color}")

                if color == "red" and deb.can_speak("red"):
                    speak("Red light. Please wait.")

                elif color == "green" and deb.can_speak("green"):
                    speak("Green light. You can cross now.")

                elif color == "yellow" and deb.can_speak("yellow"):
                    speak("Yellow light. Be careful.")

            # 🚗 VEHICLE
            if name in VEHICLE_CLASSES:
                vehicle_present = True
                draw_box(frame, xy, name)

        if vehicle_present and deb.can_speak("vehicle"):
            speak("Vehicle approaching. Do not cross.")

        cv2.imshow("BlindAssist", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

