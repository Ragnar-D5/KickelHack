import instruments
import numpy as np
from scipy import signal

INT16_LIMIT = 32768

def midi_play_sin(midi):
    return midi.synthesize(wave = np.sin)*INT16_LIMIT

def midi_play_square(midi):
    return midi.synthesize(wave = signal.square)*INT16_LIMIT

def midi_play_sawtooth(midi):
    return midi.synthesize(wave = signal.sawtooth)*INT16_LIMIT