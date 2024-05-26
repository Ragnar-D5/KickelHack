import pygame as pg
from io_functions import read_midi
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog
import play_midi
import pretty_midi
import numpy as np
from io_functions import read_midi,read_wav,debug_play_np_array
import instr.instruments
from custom_pygame_objects import DropDown

BASE_BPM = 120
BASE_TACT = 4
OCTAVE = 12

RECT_X_OFFSET = 100
RECT_Y_OFFSET = 100
RECT_WIDTH = 1720
RECT_HEIGHT = 880

KEYS = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "H",
]

class MidiTabBody:
    def __init__(self, parent):
        self.parent = parent
        
        self.notes = []
        
        self.midi = None #read_midi("test_files/TOUHOU_-_Bad_Apple.mid")
        self.instrument = None
        self.bpm = BASE_BPM
        self.play_instrument = instr.instruments.Instrument_func()
        
        self.absolute_offset = [0,-1000]
        self.previous_position = (0,0)
        
        #self.load_midi()
        
        self.file_dialog = None
        self.load_button = UIButton(relative_rect=pg.Rect(-180, -60, 150, 30),
                                    text='Load File',
                                    manager=self.parent.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'bottom': 'bottom'})
        self.drop_down = DropDown(parent=self, base_rect=pg.Rect(500,0,200,30),name="drop_down",options=["placeholder_1", "placeholder_2"])
    
    def reset(self):#reset everything
        self.parent = parent
        self.notes = []
        self.midi = None
        self.instrument = None
        self.bpm = BASE_BPM
        self.absolute_offset = [0,-1000]
        self.previous_position = (0,0)
    
    def to_midi(self,path="temp.mid"):#fill self.midi with self.notes
        self.midi = pretty_midi.PrettyMIDI()
        instrument_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
        self.instrument = pretty_midi.Instrument(program=instrument_program)
        for time_step in range(len(self.notes)):
            if hasattr(self.notes[time_step], "__len__"):
                for note in self.notes[time_step]:
                    self.instrument.notes.append(pretty_midi.Note(
                        velocity=64,
                        pitch = note,
                        start = time_step*60/self.bpm,
                        end = (time_step+1)*60/self.bpm))
        self.midi.instruments.append(self.instrument)
        self.midi.write(path)
                
    
    def synth(self):
        if self.midi != None:
            return self.midi.synthesize(fs=self.play_instrument.sample_rate,wave=self.play_instrument.wave_func)*play_midi.INT16_LIMIT
        else:
            self.to_midi()
            return self.midi.synthesize(fs=self.play_instrument.sample_rate,wave=self.play_instrument.wave_func)*play_midi.INT16_LIMIT
    
    def load_midi(self,midi):
        self.midi = midi
        self.instrument = self.midi.instruments[0]
        self.bpm = self.midi.estimate_tempo()
        self.notes = [0]*round(self.midi.get_end_time()*self.bpm)
        for note in self.instrument.notes:
            note_start = note.start / 60
            note_end = note.end/ 60
            for i in range(round(note_start*self.bpm),round(note_end*self.bpm)):#notes longer than one beat aren't currently implemented
                if self.notes[i] == 0:
                    self.notes[i] = [note.pitch]
                else:
                    self.notes[i] += [note.pitch]
    
    def ui(self, screen):
        horizontal_offset = self.absolute_offset[0] % 66
        vertical_offset = self.absolute_offset[1] % 33

        beats_since_start = -self.absolute_offset[0] / 66
        time_since_start = beats_since_start / self.bpm # in Minuten
        
        for time_step in range(max(0,round((-self.absolute_offset[0]) / (66.0))-1),min(len(self.notes),round((-self.absolute_offset[0]+ RECT_WIDTH - horizontal_offset) / (66))+1)):
            if hasattr(self.notes[time_step], "__len__"):
                for note in self.notes[time_step]:
                    left = time_step * 66 + self.absolute_offset[0] + RECT_X_OFFSET
                    top = note * 33 + self.absolute_offset[1] + RECT_Y_OFFSET
                    right = 66
                    bottom = 33
                    if left < RECT_X_OFFSET:
                        right = 66 - (RECT_X_OFFSET-left)
                        left = RECT_X_OFFSET
                    elif left + 66 > RECT_X_OFFSET + RECT_WIDTH:
                        right = RECT_X_OFFSET + RECT_WIDTH - left

                    if top < RECT_Y_OFFSET:
                        bottom = 33 - (RECT_Y_OFFSET-top)
                        top = RECT_Y_OFFSET
                    elif top + 33 > RECT_Y_OFFSET + RECT_HEIGHT:
                        bottom = RECT_Y_OFFSET + RECT_HEIGHT - top
                    
                    if bottom > 0:
                        pg.draw.rect(screen, pg.Color("red"), pg.Rect(left, top, right, bottom), 0)


        # draw vertical lines
        for i in range(1 + (RECT_WIDTH - horizontal_offset) // 66):
            point1 = pg.Vector2(RECT_X_OFFSET + horizontal_offset + i * 66, RECT_Y_OFFSET)
            point2 = pg.Vector2(RECT_X_OFFSET + horizontal_offset + i * 66, RECT_Y_OFFSET + RECT_HEIGHT-2)
            pg.draw.line(screen, pg.Color("black"), point1, point2)
            current_note = (self.absolute_offset[0]//66 - i)
            if (self.absolute_offset[0]//66 - i) % BASE_TACT == 0:
                point3 = pg.Vector2(RECT_X_OFFSET + horizontal_offset + i * 66+2, RECT_Y_OFFSET)
                point4 = pg.Vector2(RECT_X_OFFSET + horizontal_offset + i * 66+2, RECT_Y_OFFSET + RECT_HEIGHT-2)
                pg.draw.line(screen, pg.Color("black"), point3, point4)
            if pg.font:
                font = pg.font.Font(None, 32)
                note = font.render(str((-current_note)//BASE_TACT)+"."+str((-current_note)%BASE_TACT), True, (0, 0, 0))
                screen.blit(note,(RECT_X_OFFSET + horizontal_offset + i * 66 - 15,RECT_Y_OFFSET - 20))

        # draw horizontal lines
        for i in range(1 + (RECT_HEIGHT - vertical_offset) // 33):
            point1 = pg.Vector2(RECT_X_OFFSET, RECT_Y_OFFSET + vertical_offset + i * 33)
            point2 = pg.Vector2(RECT_X_OFFSET + RECT_WIDTH-5, RECT_Y_OFFSET + vertical_offset + i * 33)
            pg.draw.line(screen, pg.Color("black"), point1, point2)
            current_note = (self.absolute_offset[1]//33 - i) + 7
            if current_note % OCTAVE == 0:
                point3 = pg.Vector2(RECT_X_OFFSET, RECT_Y_OFFSET + vertical_offset + i * 33+2)
                point4 = pg.Vector2(RECT_X_OFFSET + RECT_WIDTH-5, RECT_Y_OFFSET + vertical_offset + i * 33+2)
                pg.draw.line(screen, pg.Color("black"), point3, point4)
            if pg.font:
                font = pg.font.Font(None, 32)
                note = font.render(str(-current_note//OCTAVE)+KEYS[-current_note % OCTAVE], True, (0, 0, 0))
                screen.blit(note,(RECT_X_OFFSET-50,RECT_Y_OFFSET + vertical_offset + i * 33))
        
        #draw rectangle ontop everything else
        pg.draw.rect(screen, pg.Color("black"), pg.Rect(RECT_X_OFFSET, RECT_Y_OFFSET, RECT_WIDTH, RECT_HEIGHT), 3)

    def event(self, event: pg.event.Event):
        if event.type == pg.MOUSEMOTION: #drag with middle mouse button
            
            pos = event.dict.get("pos")

            if event.dict.get("buttons")[1] == 1:
                if RECT_X_OFFSET < pos[0] and RECT_X_OFFSET + RECT_WIDTH > pos [0] and RECT_Y_OFFSET < pos[1] and RECT_Y_OFFSET + RECT_HEIGHT > pos[1]:
                    self.absolute_offset[0] += pos[0] - self.previous_position[0]
                    self.absolute_offset[1] += pos[1] - self.previous_position[1]

                    if self.absolute_offset[0] > 0:
                        self.absolute_offset[0] = 0
                    if self.absolute_offset[1] > 0:
                        self.absolute_offset[1] = 0
                    if self.absolute_offset[1] < -128 * 33 + RECT_HEIGHT:
                        self.absolute_offset[1] = -128 * 33 + RECT_HEIGHT

            self.previous_position = pos
            
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: #make note with left mouse button
                time_step = (event.pos[0] - self.absolute_offset[0] - RECT_X_OFFSET)//66
                note = (event.pos[1] - self.absolute_offset[1] - RECT_Y_OFFSET)//33
                if time_step >= 0:
                    if len(self.notes) <= time_step:
                        self.notes.extend([0]*(time_step-len(self.notes)))
                        self.notes.append([note])
                    elif self.notes[time_step] == 0:
                        self.notes[time_step] = [note]
                    elif not note in self.notes[time_step]:
                        self.notes[time_step] += [note]
            elif event.button == 3: #delete note with right mouse button
                time_step = (event.pos[0] - self.absolute_offset[0] - RECT_X_OFFSET)//66
                note = (event.pos[1] - self.absolute_offset[1] - RECT_Y_OFFSET)//33
                if len(self.notes) > time_step and time_step >=0:
                    if self.notes[time_step] != 0:
                        if note == self.notes[time_step]:
                            self.notes[time_step] = 0
                        elif note in self.notes[time_step]:
                            self.notes[time_step].remove(note)
                    

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.load_button):
            self.file_dialog = UIFileDialog(pg.Rect(160, 50, 440, 500),
                                            self.parent.ui_manager,
                                            window_title='Load File',
                                            # initial_file_path='',
                                            # allow_picking_directories=True,
                                            allow_existing_files_only=True,
                                            allowed_suffixes={".mid"})
            self.load_button.disable()

        if (event.type == pygame_gui.UI_WINDOW_CLOSE
                    and event.ui_element == self.file_dialog):
                self.load_button.enable()
                self.file_dialog = None
        
        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                self.load_midi(read_midi(event.text))
