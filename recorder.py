import os
from sound_lib import input
from sound_lib import recording
from sound_lib import stream
from sound_lib import output

i = input.Input()
o = output.Output()
class Recorder():
    def __init__(self):
        self.filename = ""
        self.recording = False
        self.s = None
    def record(self, filename):
        self.filename = filename
        self.__rec = recording.WaveRecording(filename = filename + '.wav')
        self.s = stream.FileStream(file = "start.mp3")
        self.s.play()
        self.__rec.play()
        self.recording = True
    def stop(self):
        if self.recording == True:
            self.__rec.stop()
            self.s = stream.FileStream(file = "stop.mp3")
            self.s.play()
            self.recording = False
        else:
            pass
    def play(self, count):
        try:
            if self.s.is_playing:
                self.s.stop()
                return
        except:
            pass
        if os.path.exists(count + '.wav'):
            self.s = stream.FileStream(file = count + '.wav')
            self.s.play()
        else:
            pass