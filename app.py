from flask import Flask, render_template, Response, request, jsonify
from camera import VideoCamera
import os
import time

app = Flask(__name__)
camera = None

@app.before_first_request
def init_camera():
    global camera
    camera = VideoCamera()

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frames()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/switch_mode', methods=['POST'])
def switch_mode():
    camera.switch_mode()
    return 'Mode switched', 200

@app.route('/toggle_audio', methods=['POST'])
def toggle_audio():
    camera.toggle_audio()
    return 'Audio toggled', 200

@app.route('/capture', methods=['POST'])
def capture():
    annotated_frame = camera.get_annotated_frame()
    if annotated_frame is not None:
        folder = 'screenshots'
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, f'screenshot_{int(time.time())}.jpg')
        import cv2
        cv2.imwrite(filename, annotated_frame)
        print(f"Screenshot saved: {filename}")
    else:
        print("No annotated frame available to save.")
    return 'Captured', 200

@app.route('/set_camera_source', methods=['POST'])
def set_camera_source():
    global camera
    data = request.get_json()
    source = data.get('source')
    ip = data.get('ip')
    if source == 'ip' and ip:
        camera = VideoCamera(source=f"http://{ip}/video")
    else:
        camera = VideoCamera()
    return jsonify({'status': 'Camera source updated'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)