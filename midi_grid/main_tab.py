import pygame as pg

BASE_BPM = 120
BASE_TAKT = 4

RECT_X_OFFSET = 100
RECT_Y_OFFSET = 100
RECT_WIDTH = 1720
RECT_HEIGHT = 880

class TabBody:
    def __init__(self, parent, midi_object):
        self.parent = parent

        self.midi = midi_object

        self.absolute_offset = [0,0]
        self.previous_position = (0,0)

    def ui(self, screen):
        pg.draw.rect(screen, pg.Color("black"), pg.Rect(RECT_X_OFFSET, RECT_Y_OFFSET, RECT_WIDTH, RECT_HEIGHT), 3)

        horizontal_offset = self.absolute_offset[0] % 66
        vertical_offset = self.absolute_offset[1] % 33

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

            self.previous_position = pos
