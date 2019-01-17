from face_recognition import load_image_file, face_encodings, face_locations, compare_faces
from cv2 import VideoCapture, resize

from pygame.mixer import music
from pygame import init as audio_init

from signal import signal, SIGINT
from sys import platform, argv
from sys import exit as sys_exit
from time import sleep, time
from datetime import datetime, timedelta
from subprocess import check_output, call

image_path, audio_path, wait_sec, apps = "face_irad.jpg", "alarm.wav", 5, ["Microsoft Word"]

def run(image_path, audio_path, wait_sec, apps):
    # Get a reference to webcam #0 (the default one)
    video_capture = VideoCapture(0)

    # Load pictures and learn how to recognize it.
    my_image = load_image_file(image_path)
    my_face_encoding = face_encodings(my_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [my_face_encoding]
    known_face_names = ["myself"]

    # Initialize some variables
    all_face_locations = []
    all_face_encodings = []
    face_names = []
    process_this_frame = True

    if audio_path != "skip":
        playing = False
        audio_init()
        music.load(audio_path)

    is_working = False
    start_working = time()
    end_working = start_working
    reset_working = end_working * -1

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            if platform == 'darwin' and apps:
                active_app = get_active_app()
                working_app = active_app in apps
            else:
                working_app = True
            # Find all the faces and face encodings in the current frame of video
            all_face_locations = face_locations(rgb_small_frame)
            all_face_encodings = face_encodings(rgb_small_frame, all_face_locations)

            face_names = []
            for face_encoding in all_face_encodings:
                # See if the face is a match for the known face(s)
                matches = compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)
        process_this_frame = not process_this_frame


        if "myself" in face_names and working_app:
            reset_working = time()
            if not is_working:
                start_working = time()
                is_working = True
                time_working = datetime.now()
                time_str = time_working.strftime("%d/%m/%y, %H:%M:%S")
                print()
                print("--- Started the working session  ---")
                if platform == 'darwin' and apps:
                    print(f"Working!     :), Active app: {active_app} - Time: {time_str}")
                else:
                    print(f"Working!     :) - Time: {time_str}")
                if audio_path != "skip" and playing:
                    playing = False
                    music.stop()
        else:
            end_working = time()

        now_working = time()
        elapsed_working = now_working - start_working
        elapsed_not_working = end_working - reset_working
            
        if elapsed_not_working >= wait_sec and elapsed_not_working > 0:
            if is_working:
                is_working = False
                time_stopped = datetime.now()
                time_str = time_stopped.strftime("%d/%m/%y, %H:%M:%S")
                print()
                if platform == 'darwin' and apps:
                    print(f"Not Working! :(, Active app: {active_app}  - Time: {time_str}")
                else:
                    print(f"Not Working! :( - Time: {time_str}")
                print("--- Finished the working session ---")
                if audio_path != "skip":
                    playing = True
                    music.play(-1)
        elif elapsed_working > 0:
            time_current = str_time_delta(timedelta(seconds=elapsed_working), "{hours} hours, {minutes} minutes, {seconds} seconds")
            print(f"Time Working: {time_current}", end="\r")

def str_time_delta(time_delta, fmt):
    d = {}
    d["hours"], rem = divmod(time_delta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def get_active_app():
    active_app = check_output(["osascript", "frontmost_app.applescript"]).decode().strip()
    return active_app


def signal_handler(sig, frame):
    print()
    print()
    print("---     You pressed Ctrl+C!      ---")
    print("---   Have a Nice Day! Goodbye   ---")
    sys_exit(0)


if __name__ == "__main__":
    call(["clear"],shell=True)
    signal(SIGINT, signal_handler)
    if len(argv) >= 4:
        image_path, audio_path, wait_sec = argv[1:4]
        wait_sec = int(wait_sec)
        apps = argv[4:]
    if wait_sec <= 0:
        print("Wait seconds must be bigger than 0")
        sys_exit(1)
    print("--- Welcome to Get Back To Work! ---")
    print("---  Seriously, Get Back to Work ---")
    print("---     Press Ctrl+C to quit     ---")
    print(f"--- Parameters: [Image Path: {image_path}, Audio Path: {audio_path}, Wait seconds: {wait_sec}, Apps: {apps}] ---")
    run(image_path, audio_path, wait_sec, apps)
