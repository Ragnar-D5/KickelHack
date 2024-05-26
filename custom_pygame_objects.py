import pygame as pg

class VerticalSlider(): #class to build a vertical Slider, the built-ins didn't work or weren't vertical
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


class DropDown(): #dropdown menu
    def __init__(self, parent, base_rect = pg.Rect(0,0,0,0), name = "", options=[]):
        self.parent = parent
        self.rect = base_rect
        self.name = name
        self.options = options
        self.draw_menu = False
        self.menu_activ = False
        self.active_option = -1
    
    def render(self,screen):
        pg.draw.rect(screen, "azure4", self.rect, width=0)
        font = pg.font.Font(None, 32)
        if self.active_option == -1:
            text = font.render(self.name, 1, (0, 0, 0))
        else:
            text = font.render(self.options[self.active_option], 1, (0, 0, 0))
        screen.blit(text, text.get_rect(center = self.rect.center))
        if self.draw_menu:
            for i in range(len(self.options)):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pg.draw.rect(screen, "azure3", rect, width=0)
                option = font.render(self.options[i], 1, (0, 0, 0))
                screen.blit(option, option.get_rect(center = rect.center))
    
    def event(self, event_list):#TODO: rewrite
        mpos = pg.mouse.get_pos()

        self.menu_activ = self.rect.collidepoint(mpos)
        rect = self.rect.copy()
        rect.height += len(self.options) * self.rect.height
        if self.draw_menu and rect.collidepoint(mpos):
            self.menu_activ = True
            self.active_option = -1
            for i in range(len(self.options)):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                if rect.collidepoint(mpos):
                    self.active_option = i
                    self.menu_activ = True
                    break
        elif self.rect.collidepoint(mpos):
            self.draw_menu = True
        else:
            self.draw_menu = False

        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.options[self.active_option]
        return ""
