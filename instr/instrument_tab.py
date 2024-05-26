import pygame as pg
import matplotlib
import instr.instruments
import numpy as np
import custom_pygame_objects
import matplotlib.backends.backend_agg as agg
from pygame.locals import *
import matplotlib.pyplot as plt

AMOUNT_SLIDERS = 8
RECT_X_OFFSET = 100
RECT_Y_OFFSET = 100
RECT_WIDTH = 1720
RECT_HEIGHT = 880

SLIDER_HEIGHT = 400
SLIDER_WIDTH = 10

BASE_FREQ = 440

CBLUE = (67 / 255, 82 / 255, 105 / 255)
CWHITE = (204 / 255, 220 / 255, 245 / 255)
CORANGE = (237 / 255, 152 / 255, 16 / 255)

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
    
        self.Xarray = np.linspace(0, np.pi/220, 1)
        self.Yarray = np.linspace(0, 99, 1)
    def comp_func(self,x):
        out = 0
        for i in range(AMOUNT_SLIDERS):
            out += self.vsliders[i].value*self.base_func((i+1)*x)
        return out
    
    def get_instr(self):
        return instruments.Instrument_func(self.comp_func,base_freq=BASE_FREQ)
        
    def GraphDesign(self, ax,fig):
        # Couleur du graphe, des axes:
        ax.set_facecolor(CBLUE)
        fig.patch.set_facecolor(CBLUE)
        ax.tick_params(axis='x', colors = CWHITE)
        ax.tick_params(axis='y', colors = CWHITE)
        plt.setp(ax.spines.values(), color = CWHITE)
        # Couleur des bordures du tableau:
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(2)

    def LivePlot(self, Xval, Yval, position, size, screen):
        # Nouvelle figure
        fig = plt.figure(figsize = size, dpi = 100)
        # Paramétrage:
        ax = fig.gca()
        self.GraphDesign(ax,fig)
        ax.plot(Xval, Yval, 'ro-',color = CORANGE)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, position)
        plt.close(fig)

    def update_Yarray(self):
        for index, value in enumerate(self.Xarray):
            self.Yarray[index] = self.comp_func(value)

    def ui(self,screen):
        for i in range(AMOUNT_SLIDERS):
            self.vsliders[i].render(screen)
            if pg.font:
                x,y,w,h = self.vsliders[i].rect
                screen.blit(self.slider_texts[i],(x+w/2-20,y+h+10))
        # self.LivePlot(self.Xarray, self.Yarray, (640,720), (640, 360), screen)
        self.LivePlot(self.Xarray, self.Yarray, (0,0), (100,100), screen)
    
    def event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in range(AMOUNT_SLIDERS):
                if self.vsliders[i].is_colliding(event.pos):
                    self.activ_slider = self.vsliders[i]
                    self.activ_slider.move_slider(event.pos)
                    self.update_Yarray()
        elif event.type == pg.MOUSEBUTTONUP:
            self.activ_slider = None
        
        if event.type == pg.MOUSEMOTION:
            if self.activ_slider != None:
                self.activ_slider.move_slider(event.pos)
                self.update_Yarray()
            
class VerticalSlider():
    def __init__(self, parent, base_rect = pg.Rect(0,0,0,0), value = 0.0, value_range = (0.0,1.0), slider_radius = 10):
        self.parent = parent
        self.rect = base_rect
        self.value = value
        self.value_range = value_range
        self.slider_radius = slider_radius
    
    def render(self,screen):
        pg.draw.rect(screen, pg.Color("azure4"), self.rect, width=0)
        x, y, w, h = self.rect
        if self.value_range[1]-self.value_range[0] == 0:
            pg.draw.circle(screen, pg.Color("azure3"), (x+w/2.0,y), self.slider_radius, width=0)
        pg.draw.circle(screen, pg.Color("azure3"), (x+w/2.0,y+self.value/(self.value_range[1]-self.value_range[0])*h), self.slider_radius, width=0)
    
    def move_slider(self, mouse_pos):
        x, y, w, h = self.rect
        pos = mouse_pos[1]
        #clamp the movement
        if pos < y:
            pos = y
        elif pos > y+h:
            pos = y+h
        self.value = (self.value_range[1]-self.value_range[0])*(pos-y)/h
    
    def is_colliding(self, pos):
        x, y, w, h = self.rect
        cx,cy = (x+w/2.0,y+self.value/(self.value_range[1]-self.value_range[0])*h)
        return self.rect.collidepoint(pos) or ((cx-pos[0])**2+(cy-pos[1])**2 <= self.slider_radius**2)
