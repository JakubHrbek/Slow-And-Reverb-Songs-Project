import os
from flask import Flask, request, render_template
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = 'FileProcessing'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def clear_folder(folder_path):
    """Remove all contents of the folder before processing."""
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Delete the entire folder
    os.makedirs(folder_path, exist_ok=True)  # Recreate the folder


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return "No file uploaded"

        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        if file:
            # Clear the folder before processing the file
            clear_folder(app.config['UPLOAD_FOLDER'])

            # Set the fixed filename
            new_filename = "file_processing.mp3"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

            # Save the uploaded file with the new name
            file.save(filepath)

            functionality()

            return f"File uploaded and renamed to: {new_filename}"



    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)