from io_functions import read_midi,read_wav,debug_play_np_array
import math
import numpy as np
import librosa
from scipy import signal

class Instrument_nparray:
    base_freq = 440 #in Hz
    sample_rate = 44100
    data = np.array([])
    shifted = np.array([])
    
    def __init__(self,data = np.array([]),base_freq = 440,sample_rate = 44100):
        self.data = data
        self.base_freq = base_freq
        self.sample_rate = sample_rate
        self.shifted = self.pitch_shift(440)
    
    def load_from_json(self,path): #TODO: optional cause hardcoding
        pass
    
    def pitch_shift(self,to_freq):
        return np.transpose(librosa.effects.pitch_shift(y=np.transpose(self.data).astype(float),sr=self.sample_rate,n_steps=math.log2(to_freq/self.base_freq)*12.0,bins_per_octave=12)).astype(np.short)
    
    def wave_func(self,x):
        return np.take(self.shifted,np.remainder(np.floor(16*x).astype(np.int32),self.shifted.shape[0]))
    
class Instrument_func:
    base_freq = 440 #in Hz
    sample_rate = 44100
    func = np.sin
    shifted = np.sin
    
    def __init__(self,func = np.sin,base_freq = 440,sample_rate = 44100):
        self.func = func
        self.base_freq = base_freq
        self.sample_rate = sample_rate
        self.shifted = self.pitch_shift(440)
    
    def pitch_shift(self,to_freq):
        return (lambda x: self.func(to_freq/self.base_freq*x))
    
    def wave_func(self,x):
        return self.shifted(x)
