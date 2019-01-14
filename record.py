import face_recognition
import cv2
import pyaudio  
import wave
import signal
import sys


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

def run(image_path, audio_path, wait_frames):
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load pictures and learn how to recognize it.
    my_image = face_recognition.load_image_file(image_path)
    my_face_encoding = face_recognition.face_encodings(my_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [my_face_encoding]
    known_face_names = ["myself"]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    #define stream chunk   
    chunk = 4096  

    #open a wav format music  
    f = wave.open(audio_path,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  

    playing = False
    frame_count = 0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        if "myself" in face_names:
            frame_count = 0
            if playing:
                playing = False
                #stop stream  
                stream.stop_stream()
        else:
            frame_count+=1

        if frame_count >= wait_frames:
            playing = True
            stream.start_stream()
            #read data  
            data = f.readframes(chunk)
            if not data:
                f = wave.open(audio_path,"rb")  
                data = f.readframes(chunk)
            #play stream
            stream.write(data) 


def signal_handler(sig, frame):
        print('\nYou pressed Ctrl+C!\nquitting... ')
        sys.exit(0)
    

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to quit')
    file_name, image_path, audio_path, wait_frames = sys.argv
    run(image_path, audio_path, int(wait_frames))