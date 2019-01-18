# Gannenet
Face Recognition to keep you focused on work- Playing an audio file if you don't look at your computer for a while.

![](gif/get-back-to-work.gif)

# Dependencies
## Install face_recognition:
Instructions found here- https://github.com/ageitgey/face_recognition#installation

## Install PyAudio:
Instructions found here- https://people.csail.mit.edu/hubert/pyaudio/#downloads

## Install Dash/Plotly:
Instructions found here- https://dash.plot.ly/installation + https://plot.ly/python/getting-started/#installation

# Setup
`git clone https://github.com/irad100/gannenet.git`

`cd gannenet`

Copy a picture of your face to this folder

# Run
Parameters- image file path, audio file path, seconds to wait for status change
e.g:
`python3 app.py <FACE_FILE> alarm.wav 10
## Whitelist apps
Available only for macOS.
After all the other parametes, add Apps you allow yourself to use while working.
Parameters- image file path, audio file path, seconds to wait for status change, whitelist apps
e.g:
`python3 app.py <FACE_FILE> alarm.wav 10 "Microsoft Word" "Spotify" "AdobeAcrobat" "Finder"`

# Credits
This project was created thanks to these amazing projects:

face_recognition by Adam Geitgey (ageitgey): https://github.com/ageitgey/face_recognition

(The base of my code was from here- https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py)

PyAudio by Hubert Pham: https://people.csail.mit.edu/hubert/pyaudio/

Dash by Plotly: https://plot.ly/products/dash/

