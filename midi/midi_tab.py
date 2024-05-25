import pygame as pg
import time
from io_functions import read_midi

BASE_BPM = 120
BASE_TAKT = 4

RECT_X_OFFSET = 100
RECT_Y_OFFSET = 100
RECT_WIDTH = 1720
RECT_HEIGHT = 880

class MidiTabBody:
    def __init__(self, parent, midi_object = None):
        self.parent = parent

        midi = read_midi("test_files/TOUHOU_-_Bad_Apple.mid")
        self.midi = midi
        if self.midi is not None:
            print("midi: ", self.midi.get_piano_roll())
        self.instrument = self.midi.instruments[0]
        self.bpm = self.midi.estimate_tempo()

        self.absolute_offset = [0,0]
        self.previous_position = (0,0)
        

    def ui(self, screen):
        pg.draw.rect(screen, pg.Color("black"), pg.Rect(RECT_X_OFFSET, RECT_Y_OFFSET, RECT_WIDTH, RECT_HEIGHT), 3)

        horizontal_offset = self.absolute_offset[0] % 66
        vertical_offset = self.absolute_offset[1] % 33

        beats_since_start = -self.absolute_offset[0] / 66
        time_since_start = beats_since_start / self.bpm # in Minuten

        print("----------------------------")
        for note in self.instrument.notes:
            # Zeit sei Beginn in Minuten
            note_start = note.start / 60
            note_end = note.end/ 60 
            
            if note_end > time_since_start and note_start < time_since_start + (RECT_WIDTH - horizontal_offset) / (66*self.bpm):
                if note.pitch > -self.absolute_offset[1] / 33 and note.pitch < (-self.absolute_offset[1] + RECT_HEIGHT - vertical_offset) / 33:
                    left = note_start*self.bpm * 66 + self.absolute_offset[0] + RECT_Y_OFFSET
                    top = note.pitch * 33 + self.absolute_offset[1] + RECT_X_OFFSET
                    right = 66
                    bottom = 33
                    if left < RECT_X_OFFSET:
                        left = RECT_X_OFFSET
                    elif left + 66 > RECT_X_OFFSET + RECT_WIDTH:
                        right = RECT_X_OFFSET + RECT_WIDTH - left

                    if top < RECT_Y_OFFSET:
                        top + RECT_Y_OFFSET
                    elif top + 33 > RECT_Y_OFFSET + RECT_HEIGHT:
                        bottom = RECT_Y_OFFSET + RECT_HEIGHT - top
                    pg.draw.rect(screen, pg.Color("red"), pg.Rect(left, top, right, bottom), 0)





        # draw vertical lines
        for i in range(1 + (RECT_WIDTH - horizontal_offset) // 66):
            point1 = pg.Vector2(RECT_X_OFFSET + horizontal_offset + i * 66, RECT_Y_OFFSET)
            point2 = pg.Vector2(RECT_X_OFFSET + horizontal_offset + i * 66, RECT_Y_OFFSET + RECT_HEIGHT)
            pg.draw.line(screen, pg.Color("black"), point1, point2)

        # draw horizontal lines
        for i in range(1 + (RECT_HEIGHT - vertical_offset) // 33):
            point1 = pg.Vector2(RECT_X_OFFSET, RECT_Y_OFFSET + vertical_offset + i * 33)
            point2 = pg.Vector2(RECT_X_OFFSET + RECT_WIDTH, RECT_Y_OFFSET + vertical_offset + i * 33)
            pg.draw.line(screen, pg.Color("black"), point1, point2)

    def event(self, event: pg.event.Event):
        if event.type == pg.MOUSEMOTION:

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
