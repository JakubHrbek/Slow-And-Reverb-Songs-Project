from flask import Flask, render_template, request, redirect, send_from_directory
from pydub import AudioSegment
import os

app = Flask(__name__)

# Folder where the processed files will be stored
OUTPUT_FOLDER = 'FileProcessing'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pitch_shift(audio, semitones):
    # Adjust sample rate to shift pitch
    new_sample_rate = int(audio.frame_rate * (2.0 ** (semitones / 12.0)))
    return audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(audio.frame_rate)

def remove_previous_files():
    for filename in os.listdir(OUTPUT_FOLDER):
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Remove old files from the directory
        remove_previous_files()

        filename = file.filename
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        file.save(file_path)

        try:
            audio = AudioSegment.from_file(file_path)
        except Exception as e:
            return f"Error processing the file: {e}"

        # Generate custom processed filenames
        base_filename = os.path.splitext(filename)[0]  # Get the file name without extension

        sped_up_filename = f"{base_filename}_sped_up.mp3"
        slowed_filename = f"{base_filename}_slowed_down.mp3"
        overslowed_filename = f"{base_filename}_overslowed.mp3"

        # Process the audio
        sped_up_audio = audio.speedup(playback_speed=1.15)
        slowed_audio = pitch_shift(audio, -1)
        overslowed_audio = pitch_shift(audio, -4)

        # Export the processed files with custom names
        sped_up_audio.export(os.path.join(OUTPUT_FOLDER, sped_up_filename), format="mp3")
        slowed_audio.export(os.path.join(OUTPUT_FOLDER, slowed_filename), format="mp3")
        overslowed_audio.export(os.path.join(OUTPUT_FOLDER, overslowed_filename), format="mp3")

        # Pass the custom file names to the template
        return render_template('index.html', message="Audio processing complete!",
                               processed_files=True,
                               sped_up_file=sped_up_filename,
                               slowed_down_file=slowed_filename,
                               overslowed_file=overslowed_filename)

    return "Invalid file format. Only mp3, mp4, wav, and flac are allowed."

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)