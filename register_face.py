# register_face.py
from face_recognizer import FaceRecognizer
if __name__ == '__main__':
    fr = FaceRecognizer(known_dir='known_faces')
    print('Loaded known names:', fr.known_names)
