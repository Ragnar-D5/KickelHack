import numpy as np
import librosa
from math import log2

import play_midi

def volume(np_array,dB=0):#increase/decrease volume by dB dezibells
    return np_array*(10**(dB/10))

def fade_in(np_array,rate = 44100, t = 1, f = (lambda x: x)):#fade in over t second with function f
    #check if f is valid
    g = (lambda x: x)
    if f(0) == 0 and f(t) == 1:
        g = f
        
    #fade in
    fade = np.multiply(np_array[:min(round(rate*t),np_array.shape[0])],g(np.linspace(0,1,round(rate*t)))[:min(round(rate*t),np_array.shape[0])].reshape(min(round(rate*t),np_array.shape[0]),1))
    return np.concatenate((fade,np_array[min(round(rate*t),np_array.shape[0]):]),axis=0)

def fade_out(np_array,rate = 44100, t = 1, f = (lambda x: x)):#fade out over t second with function f
    #check if f is valid
    g = (lambda x: x)
    if f(0) == 0 and f(t) == 1:
        g = f
        
    #fade out
    fade = np.multiply(np_array[max(np_array.shape[0]-round(rate*t),0):],g(np.linspace(1,0,round(rate*t)))[rate*t-min(round(rate*t),np_array.shape[0]):].reshape(min(round(rate*t),np_array.shape[0]),1))
    return np.concatenate((np_array[:max(np_array.shape[0]-round(rate*t),0)],fade),axis=0)

def echo(np_array,rate=44100,delay=1,scale=0.0,amount=0,fade=True,fade_out_time=1):#make amount echos with delay and amplitude scales down with scale
    extra_samples = round(rate*delay)*amount #how many more entries the output sample has compared to the input
    ch = 1
    if len(np_array.shape) >= 2:
        ch = np_array.shape[1]
    if fade:
        out = np.concatenate((fade_out(np_array,t=fade_out_time),np.zeros((extra_samples,ch))),axis=0)
        scaled_array = scale*fade_out(np_array,t=fade_out_time)
    else:
        out = np.concatenate((np_array,np.zeros((extra_samples,ch))),axis=0)
        scaled_array = scale*np_array
    for i in range(amount):
        out += np.concatenate((np.zeros((round(rate*delay)*(i+1),ch)),scaled_array,np.zeros((extra_samples-round(rate*delay)*(i+1),ch))),axis=0)
        scaled_array = scale*scaled_array
    return out

def speed_change(np_array,speed=1.0):
    return np.transpose(librosa.effects.time_stretch(y=np.transpose(np_array.astype(float)),rate=speed)).astype(np.short)

def pitch_shift(np_array,rate=44100,pitch=1.0):
        return np.transpose(librosa.effects.pitch_shift(y=np.transpose(np_array).astype(float),sr=rate,n_steps=log2(pitch)*12.0,bins_per_octave=12)).astype(np.short)
    
def white_noise(rate=44100,t=1,ampl=play_midi.INT16_LIMIT):
    return np.random.rand(rate*t)*ampl
