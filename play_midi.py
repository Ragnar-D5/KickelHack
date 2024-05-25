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

def midi_play_harmonic(midi,freq = [1],base_wave = np.sin):
    out = freq[0]*midi.synthesize(wave = np.sin)*INT16_LIMIT
    for i in range(1,len(freq)):
        out += freq[i]*midi.synthesize(wave = (lambda x: np.sin((i+1)*x)))*INT16_LIMIT
    return out

def midi_play_instrument(midi,instr):
    pass