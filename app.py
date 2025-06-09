from flask import Flask, request, render_template_string, send_from_directory, url_for
import os
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['FRAMES_FOLDER'] = 'frames'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['FRAMES_FOLDER'], exist_ok=True)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>🎞️ Video to Frames Converter</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
    <style>
        body {
            background: #f8f9fa;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 2rem;
        }
        .container {
            max-width: 700px;
            background: white;
            padding: 2.5rem 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgb(0 0 0 / 0.1);
        }
        h1 {
            font-weight: 700;
            color: #0d6efd;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .btn-primary {
            width: 100%;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 0.75rem;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .btn-primary:hover {
            background-color: #0b5ed7;
        }
        .message {
            margin-top: 1.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            text-align: center;
        }
        .message.success {
            color: #198754;
        }
        .message.error {
            color: #dc3545;
        }
        ul.frames-list {
            list-style-type: none;
            padding-left: 0;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 1rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #fefefe;
        }
        ul.frames-list li {
            padding: 0.5rem 1rem;
            border-bottom: 1px solid #eee;
        }
        ul.frames-list li:last-child {
            border-bottom: none;
        }
        ul.frames-list li a {
            color: #0d6efd;
            text-decoration: none;
            word-break: break-all;
        }
        ul.frames-list li a:hover {
            text-decoration: underline;
        }
        footer {
            margin-top: 3rem;
            color: #6c757d;
            font-size: 0.9rem;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container shadow-sm">
        <h1>🎞️ Video to Frames Converter</h1>
        <form method="POST" enctype="multipart/form-data" novalidate>
            <div class="mb-3">
                <label for="video" class="form-label">Select a video file</label>
                <input class="form-control" type="file" id="video" name="video" accept="video/*" required>
            </div>
            <button type="submit" class="btn btn-primary">Convert to Frames</button>
        </form>

        {% if message %}
            <p class="message success">{{ message }}</p>
            <h5>Extracted Frames:</h5>
            <ul class="frames-list">
                {% for frame in frames %}
                    <li><a href="{{ url_for('frame_file', filename=frame) }}" target="_blank">{{ frame }}</a></li>
                {% endfor %}
            </ul>
        {% endif %}
        {% if error %}
            <p class="message error">{{ error }}</p>
        {% endif %}
    </div>
    <footer>
        &copy; 2025 YourAppName. Made with ❤️ using Flask & OpenCV.
    </footer>
</body>
</html>
'''

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
    # Serve the extracted frames
    return send_from_directory(app.config['FRAMES_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    error = None
    frames = []

    if request.method == 'POST':
        if 'video' not in request.files:
            error = "Please upload a video file."
            return render_template_string(HTML, error=error)
        
        video_file = request.files['video']
        if video_file.filename == '':
            error = "No file selected."
            return render_template_string(HTML, error=error)
        
        try:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
            video_file.save(video_path)

            # Clear old frames
            for f in os.listdir(app.config['FRAMES_FOLDER']):
                os.remove(os.path.join(app.config['FRAMES_FOLDER'], f))

            total_frames = extract_frames(video_path, app.config['FRAMES_FOLDER'])
            frames = sorted(os.listdir(app.config['FRAMES_FOLDER']))

            message = f"✅ Done! Extracted {total_frames} frames."
        except Exception as e:
            error = f"❌ Error processing video: {e}"

    return render_template_string(HTML, message=message, error=error, frames=frames)

if __name__ == '__main__':
    app.run(debug=True)
