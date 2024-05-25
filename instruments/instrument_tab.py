import pygame as pg

AMOUNT_SLIDERS = 5
RECT_X_OFFSET = 100
RECT_Y_OFFSET = 100
RECT_WIDTH = 1720
RECT_HEIGHT = 880

SLIDER_HEIGHT = 400
SLIDER_WIDTH = 10

class InstrumentTabBody():
    def __init__(self, parent,current_instr=None):
        self.parent = parent
        self.current_instr = current_instr
        self.vsliders = []
        for i in range(AMOUNT_SLIDERS):
            self.vsliders += [VerticalSlider(self,pg.Rect(RECT_X_OFFSET+i/AMOUNT_SLIDERS*RECT_WIDTH,RECT_Y_OFFSET,SLIDER_WIDTH,SLIDER_HEIGHT))]
        self.activ_slider = None

    def ui(self,screen):
        for i in range(AMOUNT_SLIDERS):
            self.vsliders[i].render(screen)
    
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