from io_functions import read_midi,read_wav,debug_play_np_array
from midi.midi_tab import MidiTabBody
from arangement.arangement_tab import ArangementTabBody
from instruments.instrument_tab import InstrumentTabBody
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UIHorizontalSlider
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path
import instruments
import play_midi
import effects
import numpy as np
import scipy
from matplotlib import pyplot

class Mainwindow:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Benzaiten')
        self.window_surface = pygame.display.set_mode(size=(0,0), flags=pygame.FULLSCREEN)
        _, _, w, h = self.window_surface.get_rect()
        self.ui_manager = pygame_gui.UIManager(window_resolution=(w, h))
        self.background = pygame.Surface(size=(w, h), flags=pygame.FULLSCREEN)
        self.background.fill(self.ui_manager.ui_theme.get_colour('dark_bg'))
        self.close_button = UIButton(relative_rect=pygame.Rect(-25,0,25,25),
                                    text='X',
                                    manager=self.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'top': 'top'})

        # scale images, if necessary so that their largest dimension does not exceed these values

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.arangement_button = UIButton(pygame.Rect(0,0,100,25),"Arangement", self.ui_manager)
        self.midi_button = UIButton(pygame.Rect(100,0,100,25),"Midi", self.ui_manager)
        self.instrument_button = UIButton(pygame.Rect(200,0,100,25),"Instruments", self.ui_manager)


        # self.slider = UIHorizontalSlider(pygame.Rect((0,0),(300, 25)),25.0, (0.0,100.0), self.ui_manager, object_id="heheha")



    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.arangement_button:
                    self.active_tab = 0
                    self.arangement_tab.unhide_buttons()
                    self.midi_tab.load_button.visible = False
                elif event.ui_element == self.midi_button:
                    self.active_tab = 1
                    self.arangement_tab.hide_buttons()
                    self.midi_tab.load_button.visible = True
                elif event.ui_element == self.instrument_button:
                    self.active_tab = 2
                    self.arangement_tab.hide_buttons()
                    self.midi_tab.load_button.visible = False
                elif event.ui_element == self.close_button:
                    self.is_running = False

            if event.type == pygame.QUIT:
                self.is_running = False
            
            if self.active_tab == 0:
                self.arangement_tab.event(event)
            elif self.active_tab == 1:
                self.midi_tab.event(event)
            elif self.active_tab == 2:
                self.instrument_tab.event(event)

            self.ui_manager.process_events(event)

    def run(self):
        #tabsystem
        self.midi_tab = MidiTabBody(self)
        self.arangement_tab = ArangementTabBody(self)
        self.instrument_tab = InstrumentTabBody(self)
        
        self.active_tab = 1
        
        if self.active_tab == 0:
            self.arangement_tab.unhide_buttons()
            self.midi_tab.load_button.visible = False
        elif self.active_tab == 1:
            self.arangement_tab.hide_buttons()
            self.midi_tab.load_button.visible = True
        elif self.active_tab == 2:
            self.arangement_tab.hide_buttons()
            self.midi_tab.load_button.visible = False
            
        
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            self.process_events()
            self.ui_manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))

            if self.active_tab == 0:
                self.arangement_tab.ui(self.window_surface)
            elif self.active_tab == 1:
                self.midi_tab.ui(self.window_surface)
            elif self.active_tab == 2:
                self.instrument_tab.ui(self.window_surface)

            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    midi = read_midi("test_files/TOUHOU_-_Bad_Apple.mid")
    rate,data = read_wav("test_files/never_gonna_test.wav")
    #rate,data = read_wav("test_files/ba.wav")
    #test = instruments.Instrument_nparray(data,base_freq=123)
    #test = instruments.Instrument_func(func=np.sin,base_freq=123)
    #test = instruments.Instrument(np.sin(np.linspace(0,6.28*100,10000))*play_midi.INT16_LIMIT)
    #pyplot.plot(np.linspace(0,6.28*100,10000),np.sin(np.linspace(0,6.28*100,10000)),"-g")
    #pyplot.plot(np.linspace(0,6.28*100,10000),(lambda x: np.take(test.data,np.remainder(np.floor(15.923*x).astype(np.int16),test.data.shape[0])))(np.linspace(0,6.28*100,10000)),"-r")
    #pyplot.show()
    #print(test.data)
    #pyplot.plot(test.wave_func((np.linspace(0,1.0))),"-r")
    #pyplot.plot(test.data,"-b")
    #pyplot.show()
    #test.data = test.pitch_shift(440)
    #debug_play_np_array(effects.echo(data[50000:150000],delay=0.5,scale=0.5,amount=10),rate)
    #debug_play_np_array(effects.resample(data[50000:150000],44100,2000))
    #debug_play_np_array(effects.pitch_shift(data[50000:150000],pitch=2.0),rate)
    #debug_play_np_array(effects.white_noise()*play_midi.INT16_LIMIT,rate)
    print(midi.time_to_tick(1))
    #synth = midi.synthesize(fs=44100,wave=test.wave_func)*play_midi.INT16_LIMIT
    #debug_play_np_array(synth+effects.volume(midi.synthesize(wave = np.sin)*play_midi.INT16_LIMIT,0),44100)
    #synth = midi.synthesize(wave = np.sin)*INT16_LIMIT
    #debug_play_np_array(play_midi.midi_play_harmonic(midi,[1,0.5,0.25,0.125,0.0625]),44100)

    window_surface = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    print(window_surface.get_rect())
    app = Mainwindow()
    app.run()
