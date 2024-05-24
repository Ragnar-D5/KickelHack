from scipy.io import wavfile
from pathlib import Path
import pretty_midi

def read_wav(path):
    return wavfile.read(path)

def read_midi(path):
    return pretty_midi.PrettyMIDI(path)


