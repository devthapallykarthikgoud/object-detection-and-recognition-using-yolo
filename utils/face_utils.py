import cv2
import face_recognition
import os
from utils.speak import speak_text

known_faces = []
known_names = []

def load_known_faces():
    path = 'model/known_faces'
    for filename in os.listdir(path):
        image_path = os.path.join(path, filename)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_faces.append(encoding[0])
            known_names.append(os.path.splitext(filename)[0])

load_known_faces()

greeted = {}

def recognize_faces(frame, audio_enabled=True):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)
    detected_labels = set()

    for (top, right, bottom, left), encoding in zip(locations, encodings):
        name = "Unknown"
        matches = face_recognition.compare_faces(known_faces, encoding, tolerance=0.5)
        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]

        detected_labels.add(name)
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        if audio_enabled and name != "Unknown" and name not in greeted:
            greeted[name] = True
            speak_text(f"Hi {name}")

    return frame, detected_labels
