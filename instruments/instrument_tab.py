import pygame as pg
import matplotlib
import instruments
import numpy as np
import custom_pygame_objects

AMOUNT_SLIDERS = 8
RECT_X_OFFSET = 100
RECT_Y_OFFSET = 100
RECT_WIDTH = 1720
RECT_HEIGHT = 880

SLIDER_HEIGHT = 400
SLIDER_WIDTH = 10

BASE_FREQ = 440

class InstrumentTabBody():
    def __init__(self, parent,current_instr=None):
        self.parent = parent
        self.current_instr = current_instr
        self.vsliders = []
        self.slider_texts = []
        for i in range(AMOUNT_SLIDERS):
            self.vsliders += [custom_pygame_objects.VerticalSlider(self,pg.Rect(RECT_X_OFFSET+i/AMOUNT_SLIDERS*RECT_WIDTH,RECT_Y_OFFSET,SLIDER_WIDTH,SLIDER_HEIGHT))]
            if pg.font:
                font = pg.font.Font(None, 32)
                self.slider_texts += [font.render(str((i+1)*BASE_FREQ)+"Hz", True, (0, 0, 0))]
        self.activ_slider = None
        
        self.base_func = np.sin
    
    def comp_func(self,x):
        out = 0
        for i in range(AMOUNT_SLIDERS):
            out += self.vsliders[i].value*self.base_func((i+1)*x)
        return out
    
    def get_instr(self):
        return instruments.Instrument_func(self.comp_func,base_freq=BASE_FREQ)
        
    def ui(self,screen):
        for i in range(AMOUNT_SLIDERS):
            self.vsliders[i].render(screen)
            if pg.font:
                x,y,w,h = self.vsliders[i].rect
                screen.blit(self.slider_texts[i],(x+w/2-20,y+h+10))
    
    def event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in range(AMOUNT_SLIDERS):
                if self.vsliders[i].is_colliding(event.pos):
                    self.activ_slider = self.vsliders[i]
                    self.activ_slider.move_slider(event.pos)
        elif event.type == pg.MOUSEBUTTONUP:
            self.activ_slider = None
        
        if event.type == pg.MOUSEMOTION:
            if self.activ_slider != None:
                self.activ_slider.move_slider(event.pos)
        