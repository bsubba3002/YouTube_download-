from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>YouTube Video Downloader</title>
    <style>
        body {
            background: #121212;
            color: #eee;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 0 20px;
        }
        .container {
            background: #1e1e1e;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
            max-width: 450px;
            width: 100%;
            text-align: center;
        }
        h2 {
            margin-bottom: 24px;
            font-weight: 700;
            letter-spacing: 1.2px;
            color: #ffcc00;
        }
        input[type="text"] {
            width: 100%;
            padding: 14px 16px;
            font-size: 1rem;
            border-radius: 8px;
            border: none;
            margin-bottom: 18px;
            background: #2c2c2c;
            color: #eee;
            box-sizing: border-box;
            outline: none;
            transition: background 0.3s ease;
        }
        input[type="text"]:focus {
            background: #3d3d3d;
        }
        input[type="submit"] {
            background: #ffcc00;
            border: none;
            color: #121212;
            font-weight: 700;
            font-size: 1.1rem;
            padding: 14px 20px;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
            width: 100%;
        }
        input[type="submit"]:hover {
            background: #e6b800;
        }
        p.message {
            margin-top: 20px;
            font-weight: 600;
            font-size: 1rem;
            color: #90ee90; /* green */
        }
        p.error {
            color: #ff4c4c; /* red */
        }
        @media (max-width: 500px) {
            .container {
                padding: 20px;
            }
            input[type="text"], input[type="submit"] {
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Video Downloader</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Enter YouTube video URL" required>
            <input type="submit" value="Download">
        </form>
        {% if message %}
            <p class="message {{ 'error' if 'Error' in message else '' }}">{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            yt_dlp.YoutubeDL().download([url])
            message = "✅ Video downloaded successfully!"
        except Exception as e:
            message = f"❌ Error: {e}"
    return render_template_string(HTML_FORM, message=message)

if __name__ == '__main__':
    app.run(debug=True)
