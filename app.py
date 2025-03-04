from flask import Flask, render_template, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-jarvis')
def start_jarvis():
    subprocess.Popen(["python", "jarvis.py"])
    return "Jarvis started!"

@app.route('/get-response')
def get_response():
    """Serve the latest voice response."""
    audio_file = "static/response.mp3"
    if os.path.exists(audio_file):
        return send_file(audio_file, mimetype="audio/mp3")
    return "No response yet", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)








