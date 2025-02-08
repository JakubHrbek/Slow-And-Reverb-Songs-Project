import os
import subprocess
import webbrowser
import time

# Define the directory where your Flask app is located
app_directory = "/Users/jakubhrbek/Desktop/GitHub-Project/Slow-And-Reverb-Songs-Project/myproject"  # Path to your app

# Change the current working directory to the Flask app directory
os.chdir(app_directory)

# Run `flask run` in a subprocess (background process)
subprocess.Popen(["flask", "run"])

# Wait a few seconds for Flask to start
time.sleep(3)  # You can adjust the sleep time depending on how long Flask takes to start

# Open the web browser at the Flask app's URL
webbrowser.open("http://127.0.0.1:5000")