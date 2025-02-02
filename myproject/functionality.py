import tkinter as tk
from tkinter import filedialog
import os
import soundfile as sf
import pyrubberband as pyrb

def process_file(file_path):
    print(f"Processing file: {file_path}")

    # Make folder
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

    # Folder name
    folder_name = "MyNewFolder"

    # Full path for the new folder
    folder_path = os.path.join(desktop_path, folder_name)

    # Create the folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created on the Desktop.")
    else:
        print(f"Folder '{folder_name}' already exists.")

    y, sr = sf.read(file_path)
    y_stretch = pyrb.time_stretch(y, sr, 2.0)
    y_stretch = pyrb.time_stretch(y, sr, 2.0, rbargs={'-c': '5', '--no_transients': ''})

    # Generate the output file path
    output_file_path = os.path.join(folder_path, "stretched_audio.wav")

    # Export the stretched audio to the new file
    sf.write(output_file_path, y_stretch, sr)
    print(f"Stretched audio saved to: {output_file_path}")

root = tk.Tk()
root.withdraw()

# Open file dialog to choose a file
file_path = filedialog.askopenfilename()

if file_path:
    process_file(file_path)
else:
    print("No file selected.")

root.mainloop()