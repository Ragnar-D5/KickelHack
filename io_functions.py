from scipy.io import wavfile
from pathlib import Path
import pretty_midi
import pyaudio

def read_wav(path):
    return wavfile.read(path)

def read_midi(path):
    return pretty_midi.PrettyMIDI(path)


def debug_play_np_array(np_array,wav_rate=44100):
    stream = pyaudio.PyAudio().open(rate=wav_rate, format=pyaudio.paInt16, channels=int(np_array.shape[1]), output=True)
    stream.write(np_array.tobytes())
    stream.close() # this blocks until sound finishes playing
    pyaudio.PyAudio().terminate()


