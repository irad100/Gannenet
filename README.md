# Get Back To Work!
Face Recognition software to keep you focused on work- Playing an audio file if you don't look at your computer for a while.

![](get-back-to-work.gif)

# Dependencies
## Install face_recognition:
Instruction found here- https://github.com/ageitgey/face_recognition#installation

## Install PyAudio:
Instruction found here- https://people.csail.mit.edu/hubert/pyaudio/#downloads

# Setup
`git clone https://github.com/irad100/get-back-to-work.git`

`cd get-back-to-work`

Copy a picture of your face to this folder

# Run
Parameters- your image, audio file, frames to wait till audio

`python3 record.py <FACE_FILE> just-do-it.wav 1`

# Credits
This project was created thanks to these amazing projects

face_recognition by Adam Geitgey (ageitgey): https://github.com/ageitgey/face_recognition

(I used alot of the code from here- https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py)

PyAudio by Hubert Pham: https://people.csail.mit.edu/hubert/pyaudio/
