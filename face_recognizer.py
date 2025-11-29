# face_recognizer.py (uses face_recognition as fallback if MobileFaceNet not ready)
import os
import numpy as np
import face_recognition

class FaceRecognizer:
    def __init__(self, known_dir="known_faces", mobilefacenet_onnx=None):
        self.known_dir = known_dir
        self.known_encodings = []
        self.known_names = []
        self._load_known_faces()

    def _load_known_faces(self):
        if not os.path.exists(self.known_dir):
            os.makedirs(self.known_dir)
        for person in os.listdir(self.known_dir):
            person_dir = os.path.join(self.known_dir, person)
            if not os.path.isdir(person_dir):
                continue
            for fname in os.listdir(person_dir):
                path = os.path.join(person_dir, fname)
                try:
                    img = face_recognition.load_image_file(path)
                    encs = face_recognition.face_encodings(img)
                    if len(encs) > 0:
                        self.known_encodings.append(encs[0])
                        self.known_names.append(person)
                        print(f"Loaded encoding for {person} from {fname}")
                except Exception as e:
                    print("Failed to load", path, e)

    def recognize(self, frame, face_box):
        x1, y1, x2, y2 = map(int, face_box)
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = max(0, x2), max(0, y2)
        crop = frame[y1:y2, x1:x2]
        if crop.size == 0:
            return None
        rgb = crop[:, :, ::-1]
        encs = face_recognition.face_encodings(rgb)
        if len(encs) == 0:
            return None
        enc = encs[0]
        if len(self.known_encodings) == 0:
            return None
        matches = face_recognition.compare_faces(self.known_encodings, enc, tolerance=0.5)
        if True in matches:
            idx = matches.index(True)
            return self.known_names[idx]
        dists = face_recognition.face_distance(self.known_encodings, enc)
        if len(dists) > 0:
            best_idx = int(np.argmin(dists))
            if dists[best_idx] < 0.45:
                return self.known_names[best_idx]
        return None
