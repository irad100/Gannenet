# Gannenet

Face Recognition to keep you focused on work- Playing an audio file if you don't look at your computer for a while.

![gif](images/get-back-to-work.gif)

## Dependencies

### Install face_recognition

Instructions found here- https://github.com/ageitgey/face_recognition#installation

### Install PyAudio

Instructions found here- https://people.csail.mit.edu/hubert/pyaudio/#downloads

### Install Dash/Plotly

Instructions found here- https://dash.plot.ly/installation + https://plot.ly/python/getting-started/#installation

### To Install all automatically

After installing PortAudio and dlib for your system run:

`pip install -r requirements.txt`

## Setup

`git clone https://github.com/irad100/gannenet.git`

`cd gannenet`

Copy a picture of your face to the images folder

## Run

Parameters- image file path, audio file path, seconds to wait for status change

e.g:

`python3 app.py images/<FACE_FILE> audio/alarm.wav 10`

### Whitelist apps

Available only for macOS.

After all the other parametes, add Apps you allow yourself to use while working.

Parameters- image file path, audio file path, seconds to wait for status change, whitelist apps

e.g:

`python3 app.py images/<FACE_FILE> audio/alarm.wav 10 "Microsoft Word" "Spotify" "AdobeAcrobat" "Finder"`

Note: To find out what is the appropriate name for each app you can run:

`while true; do sleep 1; osascript scripts/active_app.applescript; done`

Then switch to the wanted app

## Credits

This project was created thanks to these amazing projects:

face_recognition by Adam Geitgey (ageitgey): https://github.com/ageitgey/face_recognition

(The base of my code was from here- https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py)

PyAudio by Hubert Pham: https://people.csail.mit.edu/hubert/pyaudio/

Dash by Plotly: https://plot.ly/products/dash/
