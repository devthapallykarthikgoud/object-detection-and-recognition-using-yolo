import cv2
from ultralytics import YOLO
from utils.face_utils import recognize_faces
from utils.speak import speak_text
from utils.tracker import ObjectTracker
import threading
import time

class VideoCamera:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        self.model = YOLO('yolov8n.pt')
        self.tracker = ObjectTracker()
        self.mode = 'object'
        self.audio_enabled = True
        self.last_spoken = {}
        self.last_reset_time = time.time()
        self.frame = None
        self.annotated_frame = None

    def switch_mode(self):
        self.mode = 'face' if self.mode == 'object' else 'object'

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled

    def get_frames(self):
        success, frame = self.cap.read()
        if not success:
            print("[ERROR] Failed to read frame from camera.")
            return None

        self.frame = frame.copy()
        self.annotated_frame, labels = self.process_frame(frame)

        if self.audio_enabled:
            now = time.time()
            if now - self.last_reset_time > 10:
                self.last_spoken.clear()
                self.last_reset_time = now
            for label in labels:
                if label not in self.last_spoken:
                    self.last_spoken[label] = now
                    threading.Thread(target=speak_text, args=(label,)).start()

        ret, jpeg = cv2.imencode('.jpg', self.annotated_frame)
        if not ret:
            print("[ERROR] Failed to encode frame to JPEG.")
            return None

        return jpeg.tobytes()

    def process_frame(self, frame):
        labels = set()
        annotated_frame = frame.copy()

        if self.mode == 'object':
            results = self.model(frame, stream=False)[0]
            for box in results.boxes:
                conf = float(box.conf[0])
                if conf < 0.4:
                    continue
                cls = int(box.cls[0])
                label = self.model.names[cls]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                labels.add(label)
        elif self.mode == 'face':
            annotated_frame, face_labels = recognize_faces(annotated_frame, self.audio_enabled)
            labels.update(face_labels)

        return annotated_frame, labels

    def capture_frame(self):
        return self.frame

    def get_annotated_frame(self):
        return self.annotated_frame