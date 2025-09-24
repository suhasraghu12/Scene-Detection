import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_scene_changes_frame_diff(video_path, threshold=30):
    """
    Detects scene changes in a video using frame differencing.

    Args:
        video_path (str): Path to the video file.
        threshold (int): Pixel intensity difference threshold for scene change detection.

    Returns:
        tuple: A list of frame numbers and timestamps where scene changes are detected.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return [], []

    scene_changes_frames = []
    ret, prev_frame = cap.read()
    if not ret:
        cap.release()
        return [], []

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_count = 1

    while True:
        ret, current_frame = cap.read()
        if not ret:
            break

        current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(current_gray, prev_gray)
        mean_diff = np.mean(diff)

        if mean_diff > threshold:
            scene_changes_frames.append(frame_count)

        prev_gray = current_gray
        frame_count += 1

    fps = cap.get(cv2.CAP_PROP_FPS)
    scene_changes_timestamps = [frame_num / fps for frame_num in scene_changes_frames]
    cap.release()
    return scene_changes_frames, scene_changes_timestamps

def process_video_for_frontend(video_path, threshold=30):
    """
    Processes a video for scene change detection and generates visualizations.

    Args:
        video_path (str): Path to the video file.
        threshold (int): Pixel intensity difference threshold.

    Returns:
        tuple: Frame numbers, timestamps, and base64-encoded image data.
    """
    scene_changes_frames, scene_changes_timestamps = detect_scene_changes_frame_diff(video_path, threshold)
    visualization_data = []

    if scene_changes_frames:
        cap = cv2.VideoCapture(video_path)
        if cap.isOpened():
            for frame_num, timestamp in zip(scene_changes_frames, scene_changes_timestamps):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num - 1)
                ret, frame = cap.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    plt.figure()
                    plt.imshow(frame_rgb)
                    plt.title(f"Scene Change at Frame {frame_num} ({timestamp:.2f} seconds)")
                    plt.axis('off')
                    buf = BytesIO()
                    plt.savefig(buf, format='png')
                    buf.seek(0)
                    plt.close()
                    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                    visualization_data.append(img_base64)
            cap.release()

    return scene_changes_frames, scene_changes_timestamps, visualization_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'video' not in request.files:
            return render_template('index.html', error="No video file uploaded.")
        
        file = request.files['video']
        if file.filename == '':
            return render_template('index.html', error="No video file selected.")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(video_path)

            # Process the video
            frames, timestamps, visualizations = process_video_for_frontend(video_path)
            
            # Clean up the uploaded file
            os.remove(video_path)

            return render_template('index.html',
                                 frames=frames,
                                 timestamps=[f"{t:.2f}" for t in timestamps],
                                 visualizations=visualizations,
                                 error=None)
    
    return render_template('index.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)