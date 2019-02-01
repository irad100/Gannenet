from threading import Thread

from face_recognition import load_image_file, face_encodings, face_locations, compare_faces
from cv2 import VideoCapture, resize

import audio
from threading import Thread

import sys
from signal import signal, SIGINT
from time import sleep, time
from datetime import datetime, timedelta
from subprocess import check_output, call


class Gannenet(Thread):
    exit = False
    #today_date = datetime.now().date().isoformat()
    #sys.stdout = open(f'{today_date}.log', 'w')
    is_working = False
    start_working = datetime.now()
    end_working = start_working
    reset_working = start_working

    elapsed_working = 0
    elapsed_not_working = 0
    elapsed = 0

    video_capture = None
    my_image = None
    my_face_encoding = None
    known_face_encodings = []
    known_face_names = []
    all_face_locations = []
    all_face_encodings = []
    face_names = []
    process_this_frame = True
    playing = False
    player = None
    image_path, audio_path, wait_sec, apps = "", "", 0, []
    is_gui = True

    def __init__(self, image_path="images/face_irad.jpg", audio_path="audio/alarm.wav", wait_sec=10, apps=["Microsoft Word", "Microsoft Excel", "Spotify", "AdobeAcrobat", "Finder"], is_gui=True):
        super(Gannenet, self).__init__()
        self.is_gui = is_gui
        self.image_path, self.audio_path, self.wait_sec, self.apps = image_path, audio_path, wait_sec, apps
        if not self.is_gui:
            print("--- Welcome to Get Back To Work! ---")
            print("---  Seriously, Get Back to Work ---")
            print("---     Press Ctrl+C to quit     ---")
            print(
                f"--- Parameters: [Image Path: {self.image_path}, Audio Path: {self.audio_path}, Wait seconds: {self.wait_sec}, self.apps: {self.apps}] ---\n")
        # Get a reference to webcam #0 (the default one)
        self.video_capture = VideoCapture(0)

        # Load pictures and learn how to recognize it.
        self.my_image = load_image_file(self.image_path)
        self.my_face_encoding = face_encodings(self.my_image)[0]

        # Create arrays of known face encodings and their names
        self.known_face_encodings = [self.my_face_encoding]
        self.known_face_names = ["myself"]

        if self.audio_path != "skip":
            self.playing = False
            self.player = audio.Player(self.audio_path)

    def run(self):
        while not self.exit:
            # Grab a single frame of video
            ret, frame = self.video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if self.process_this_frame:
                if sys.platform == 'darwin' and self.apps:
                    active_app = self.get_active_app()
                    working_app = active_app in self.apps
                else:
                    working_app = True
                # Find all the faces and face encodings in the current frame of video
                self.all_face_locations = face_locations(rgb_small_frame)
                self.all_face_encodings = face_encodings(
                    rgb_small_frame, self.all_face_locations)

                self.face_names = []
                for face_encoding in self.all_face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = compare_faces(
                        self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    # If a match was found in self.known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.known_face_names[first_match_index]

                    self.face_names.append(name)
            self.process_this_frame = not self.process_this_frame

            if "myself" in self.face_names and working_app:
                self.reset_working = datetime.now()
                if not self.is_working:
                    self.start_working = datetime.now()
                    self.is_working = True
                    if not self.is_gui:
                        time_str = self.start_working.strftime(
                            "%d/%m/%y, %H:%M:%S")
                        print("\n\n\n--- Started the working session  ---\n")
                        if sys.platform == 'darwin' and self.apps:
                            print(
                                f"Working!     :), Active app: {active_app} - Time: {time_str}\n")
                        else:
                            print(f"Working!     :) - Time: {time_str}\n")
                    if self.audio_path != "skip" and self.playing:
                        self.playing = False
                        self.player.stop()

            now_working = datetime.now()
            self.elapsed_working = (
                now_working - self.start_working).total_seconds()
            self.elapsed_not_working = (
                now_working - self.reset_working).total_seconds()

            if self.elapsed_not_working >= self.wait_sec and self.elapsed_not_working > 0:
                if self.is_working:
                    self.end_working = datetime.now()
                    self.reset_working = self.end_working
                    self.is_working = False
                    if not self.is_gui:
                        time_str = self.end_working.strftime(
                            "%d/%m/%y, %H:%M:%S")
                        if sys.platform == 'darwin' and self.apps:
                            print(
                                f"\n\nNot Working! :(, Active app: {active_app}  - Time: {time_str}\n")
                        else:
                            print(f"\n\nNot Working! :( - Time: {time_str}\n")
                            print("--- Finished the working session ---\n\n")
                    if self.audio_path != "skip":
                        self.playing = True
                        self.player = audio.Player(self.audio_path)
                        self.player.play()
            if not self.is_gui:
                print(self.to_string(), end="\r")

    def __str_time_delta(self, time_delta, fmt):
        d = {}
        d["hours"], rem = divmod(time_delta.seconds, 3600)
        d["minutes"], d["seconds"] = divmod(rem, 60)
        return fmt.format(**d)

    def get_active_app(self):
        active_app = check_output(
            ["osascript", "scripts/active_app.applescript"]).decode().strip()
        return active_app

    def get_work_status(self):
        return self.is_working

    def get_working_session_times(self):
        return self.start_working, self.end_working

    def to_string(self):
        work_status_bool = self.get_work_status()
        if work_status_bool:
            self.elapsed = self.elapsed_working
        else:
            self.elapsed = self.elapsed_not_working
        time_current = self.__str_time_delta(timedelta(
            seconds=self.elapsed), "{hours} hours, {minutes} minutes, {seconds} seconds")
        work_status_dir = {True: "Working", False: "Not Working"}
        work_status = work_status_dir[work_status_bool]
        return f"Time {work_status}: {time_current}"

    def stop(self):
        """
        Stop playback.
        """
        if self.audio_path != 'skip':
            self.player.stop()
        self.exit = True


def __signal_handler(sig, frame):
    print("\n\n\n---     You pressed Ctrl+C!      ---")
    print("---   Have a Nice Day! Goodbye   ---")
    g.exit()
    sys.exit(0)


if __name__ == "__main__":
    call(["clear"], shell=True)
    signal(SIGINT, __signal_handler)
    if len(sys.argv) >= 4:
        image_path, audio_path, wait_sec = sys.argv[1:4]
        wait_sec = int(wait_sec)
        apps = sys.argv[4:]
        if wait_sec <= 0:
            print("Wait seconds must be bigger than 0")
            sys.exit(1)
        g = Gannenet(image_path=image_path, audio_path=audio_path,
                     wait_sec=wait_sec, apps=apps, is_gui=False)
    else:
        g = Gannenet(is_gui=False)
    g.start()
