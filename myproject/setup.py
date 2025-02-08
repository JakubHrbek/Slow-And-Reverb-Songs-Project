from setuptools import setup

APP = ['app.py']  # replace with the name of your Flask script
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['flask', 'your-dependencies'],  # Add any required packages here
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)