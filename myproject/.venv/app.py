import os
from flask import Flask, request, render_template, send_file
from pydub import AudioSegment
import tempfile

app = Flask(__name__)

# Configure upload folder (where uploaded files are temporarily stored)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed extensions for file upload
ALLOWED_EXTENSIONS = {'mp3'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if the file part is in the request
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        # If no file is selected
        if file.filename == '':
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the uploaded file (e.g., slow down and apply reverb)
            processed_filepath = process_audio(filepath)

            # Send the processed file to the user
            return send_file(processed_filepath, as_attachment=True)

    return render_template("index.html")


def process_audio(input_path):
    # Load the uploaded MP3 file using pydub
    audio = AudioSegment.from_mp3(input_path)

    # Example processing: slow it down (50% slower)
    slowed_audio = audio.speedup(playback_speed=0.5)

    # Example: Save the processed audio to a temporary file
    temp_output = tempfile.mktemp(suffix=".mp3")
    slowed_audio.export(temp_output, format="mp3")

    # You could add more processing (e.g., reverb) here

    return temp_output


if __name__ == "__main__":
    app.run(debug=True)