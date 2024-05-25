import math
import numpy as np
import librosa

class Instrument:
    base_freq = 440 #in Hz
    sample_rate = 44100
    data = np.array([])
    
    def __init__(self,data = np.array([]),base_freq = 440,sample_rate = 44100):
        self.data = data
    
    def load_from_json(self,path): #TODO: optional cause hardcoding
        pass
    
    def pitch_shift(self,to_freq): #TODO: fix
        #pitch_shift returns half the sample_rate for some reason, stereo issue?
        return np.transpose(librosa.effects.pitch_shift(y=np.transpose(self.data).astype(float),sr=self.sample_rate,n_steps=math.log2(to_freq/self.base_freq)*12.0,bins_per_octave=12)).astype(np.short)