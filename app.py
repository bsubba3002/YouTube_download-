from flask import Flask, request, render_template, send_from_directory
import os
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['FRAMES_FOLDER'] = 'frames'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['FRAMES_FOLDER'], exist_ok=True)

def extract_frames(video_path, frames_folder):
    cap = cv2.VideoCapture(video_path)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        filename = os.path.join(frames_folder, f'frame_{count:05d}.jpg')
        cv2.imwrite(filename, frame)
        count += 1
    cap.release()
    return count

@app.route('/frames/<filename>')
def frame_file(filename):
    return send_from_directory(app.config['FRAMES_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    error = None
    frames = []

    if request.method == 'POST':
        if 'video' not in request.files:
            error = "Please upload a video file."
            return render_template("index.html", error=error)
        
        video_file = request.files['video']
        if video_file.filename == '':
            error = "No file selected."
            return render_template("index.html", error=error)
        
        try:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
            video_file.save(video_path)

            # Clear previous frames
            for f in os.listdir(app.config['FRAMES_FOLDER']):
                os.remove(os.path.join(app.config['FRAMES_FOLDER'], f))

            total_frames = extract_frames(video_path, app.config['FRAMES_FOLDER'])
            frames = sorted(os.listdir(app.config['FRAMES_FOLDER']))
            message = f"✅ Done! Extracted {total_frames} frames."

        except Exception as e:
            error = f"❌ Error processing video: {e}"

    return render_template("index.html", message=message, error=error, frames=frames)

if __name__ == '__main__':
    app.run(debug=True)
