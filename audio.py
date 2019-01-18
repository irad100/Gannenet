from threading import Thread
from wave import open as wave_open
from pyaudio import PyAudio

class Player(Thread):
    audio_path = ""
    chunk = 0
    p = None
    stream = None
    wave_obj = None
    loop = True

    def __init__(self, audio_path):
        super(Player, self).__init__()
        self.audio_path = audio_path
        # define stream chunk
        self.chunk = 1024
        # open a wav format music
        self.wave_obj = wave_open(audio_path, "rb")
        # instantiate PyAudio
        self.p = PyAudio()
        # open stream
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wave_obj.getsampwidth()),
                                  channels=self.wave_obj.getnchannels(),
                                  rate=self.wave_obj.getframerate(),
                                  output=True)

    def run(self):
        while self.loop:
            self.stream.start_stream()
            data = self.wave_obj.readframes(self.chunk)
            if not data:
                self.wave_obj.rewind()
                data = self.wave_obj.readframes(self.chunk)
            self.stream.write(data)

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def play(self):
        """
        Just another name for self.start()
        """
        self.start()

    def stop(self):
        """
        Stop playback.
        """
        self.loop = False

