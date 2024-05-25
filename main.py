from io_functions import read_midi,read_wav,debug_play_np_array
from midi.midi_tab import MidiTabBody
from arangement.arangement_tab import ArangementTabBody
from instruments.instrument_tab import InstrumentTabBody
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path
import instruments
import play_midi
import effects
import numpy as np
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
        self.load_button = UIButton(relative_rect=pygame.Rect(-180, -60, 150, 30),
                                    text='Load File',
                                    manager=self.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'bottom': 'bottom'})

        self.file_dialog = None

        # scale images, if necessary so that their largest dimension does not exceed these values

        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self):
        midi_tab = MidiTabBody(self)
        arangement_tab = ArangementTabBody(self)
        instrument_tab = InstrumentTabBody(self)

        active_tab = 1
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.load_button):
                    self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                                    self.ui_manager,
                                                    window_title='Load File',
                                                    # initial_file_path='',
                                                    # allow_picking_directories=True,
                                                    allow_existing_files_only=True,
                                                    allowed_suffixes={""})
                    self.load_button.disable()

                if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                    if self.display_loaded_image is not None:
                        self.display_loaded_image.kill()

                if (event.type == pygame_gui.UI_WINDOW_CLOSE
                        and event.ui_element == self.file_dialog):
                    self.load_button.enable()
                    self.file_dialog = None

                if active_tab == 0:
                    arangement_tab.event()
                elif active_tab == 1:
                    midi_tab.event(event)
                elif active_tab == 2:
                    instrument_tab.event(event)

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))

            if active_tab == 0:
                arangement_tab.ui()
            elif active_tab == 1:
                midi_tab.ui(self.window_surface)
            elif active_tab == 2:
                instrument_tab.ui()

            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()

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
    
    debug_play_np_array(effects.echo(data[50000:150000],delay=0.5,scale=0.5,amount=10),rate)
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
