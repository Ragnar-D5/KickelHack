import pygame as pg
from io_functions import read_midi,write_wav,read_wav
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog
import numpy as np
import sounddevice as sd
import play_midi

TIMELINE_LENGTH = 10 #in seconds
CHANNEL_HEIGHT = 100

RECT_X_OFFSET = 150
RECT_Y_OFFSET = 100
RECT_WIDTH = 1220
RECT_HEIGHT = 880


class ArangementTabBody():
    def __init__(self, parent):
        self.parent = parent
        
        self.sample_rate = 44100
        
        #the place where everything sound is stored (in stereo)
        self.sound = np.array([])
        
        #contains the blocks (in chronological order if we had more time)
        self.blocks = []
        self.active_block = None
        
        self.absolute_offset = [0,0]
        self.previous_position = (0,0)
        
        self.buttons = {
            "load_button":UIButton(relative_rect=pg.Rect(-180, -60, 150, 30),
                                    text='Load File',
                                    manager=self.parent.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'bottom': 'bottom'}),
            "midi_block_button":UIButton(relative_rect=pg.Rect(-180, -100, 150, 30),
                                    text='Midi Block',
                                    manager=self.parent.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'bottom': 'bottom'}),
            "play_sound_button":UIButton(relative_rect=pg.Rect(-180, -140, 150, 30),
                                    text='Play sound',
                                    manager=self.parent.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'bottom': 'bottom'}),
            "stop_sound_button":UIButton(relative_rect=pg.Rect(-180, -180, 150, 30),
                                    text='Stop sound',
                                    manager=self.parent.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'bottom': 'bottom'}),
            "export_wav_button":UIButton(relative_rect=pg.Rect(-180, -220, 150, 30),
                                    text='export wavy.wav',
                                    manager=self.parent.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'bottom': 'bottom'})
        }
        self.file_dialog = None
        
        self.old_block_range = (0,0)
    
    def recalculate(self,sample_range=(0,0)):
        out_range = np.zeros((round(sample_range[1]*self.sample_rate-sample_range[0]*self.sample_rate),2))
        for bl in self.blocks:
            if bl.t <= sample_range[1] and bl.get_end_time() >= sample_range[0]:
                for i in range(0,round(bl.get_end_time()*self.sample_rate-bl.t*self.sample_rate)):
                    if len(bl.data) > i:
                        if hasattr(bl.data[i], "__len__"):
                            out_range[i][0] += bl.data[i][0]
                            out_range[i][1] += bl.data[i][1]
                        else:
                            out_range[i][0] += bl.data[i]
                            out_range[i][1] += bl.data[i]
#         if sample_range[0] == 0:
#             if out_range == []:
#                 if sample_range[1] == len(self.sound)-1:
#                     self.sound = np.array([])
#                 self.sound = np.concatenate(self.sound[sample_range[1]:])
#             self.sound = np.concatenate(out_range,self.sound[sample_range[1]:])
        if len(self.sound.shape) == 1:
            self.sound = np.transpose(np.tile(self.sound, (2, 1)))
            
        self.sound = np.concatenate((self.sound[:int(sample_range[0]*self.sample_rate)],out_range,self.sound[int(sample_range[1]*self.sample_rate):]))
                
    
    def hide_buttons(self):
        for btn in self.buttons.values():
            btn.visible = False
    def unhide_buttons(self):
        for btn in self.buttons.values():
            btn.visible = True    
    
    def ui(self,screen):
        px_per_sec = round(RECT_WIDTH/TIMELINE_LENGTH)
        for bl in self.blocks:
            if bl.t*px_per_sec+self.absolute_offset[0] >= -(bl.data.shape[0]/bl.sample_rate)*px_per_sec and bl.t*px_per_sec+self.absolute_offset[0] <= RECT_WIDTH:
                if (bl.ch)*CHANNEL_HEIGHT+self.absolute_offset[1] >= 0  and (bl.ch-1)*CHANNEL_HEIGHT+self.absolute_offset[1] <=  RECT_HEIGHT:
                    bl.render(screen)
        
        # draw horizontal lines
        for i in range(1 + (RECT_HEIGHT - self.absolute_offset[1]%CHANNEL_HEIGHT) // CHANNEL_HEIGHT):
            point1 = pg.Vector2(RECT_X_OFFSET, RECT_Y_OFFSET + self.absolute_offset[1]%CHANNEL_HEIGHT + i * CHANNEL_HEIGHT)
            point2 = pg.Vector2(RECT_X_OFFSET + RECT_WIDTH-5, RECT_Y_OFFSET + self.absolute_offset[1]%CHANNEL_HEIGHT + i * CHANNEL_HEIGHT)
            pg.draw.line(screen, pg.Color("black"), point1, point2)
            if pg.font:
                font = pg.font.Font(None, 32)
                note = font.render("Channel "+str(i-(self.absolute_offset[1]) // CHANNEL_HEIGHT), True, (0, 0, 0))
                screen.blit(note,(0,RECT_Y_OFFSET + self.absolute_offset[1]%CHANNEL_HEIGHT + i * CHANNEL_HEIGHT - CHANNEL_HEIGHT/2))
                
        # draw vertical lines
        horizontal_offset = self.absolute_offset[0]%px_per_sec
        for i in range(1 + (RECT_WIDTH - self.absolute_offset[0]%px_per_sec) // px_per_sec):
            point1 = pg.Vector2(RECT_X_OFFSET + horizontal_offset + i * px_per_sec, RECT_Y_OFFSET)
            point2 = pg.Vector2(RECT_X_OFFSET + horizontal_offset + i * px_per_sec, RECT_Y_OFFSET + RECT_HEIGHT-2)
            pg.draw.line(screen, pg.Color("gray20"), point1, point2)
            if pg.font:
                font = pg.font.Font(None, 32)
                note = font.render(str(i-self.absolute_offset[0] // px_per_sec)+" s", True, (0, 0, 0))
                screen.blit(note,(RECT_X_OFFSET + horizontal_offset + i * px_per_sec - 15,RECT_Y_OFFSET - 20))
                

    def event(self, event):
        if event.type == pg.MOUSEMOTION: #drag stuff
            if self.active_block != None:
                self.active_block.move(event.pos)
            else:
                pos = event.dict.get("pos")

                if event.dict.get("buttons")[1] == 1:
                    if RECT_X_OFFSET < pos[0] and RECT_X_OFFSET + RECT_WIDTH > pos [0] and RECT_Y_OFFSET < pos[1] and RECT_Y_OFFSET + RECT_HEIGHT > pos[1]:
                        self.absolute_offset[0] += pos[0] - self.previous_position[0]
                        self.absolute_offset[1] += pos[1] - self.previous_position[1]

                        if self.absolute_offset[0] > 0:
                            self.absolute_offset[0] = 0

                self.previous_position = pos
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for bl in self.blocks:
                    if bl.is_colliding(event.pos):
                        self.old_block_range = (bl.t,bl.get_end_time())
                        self.active_block = bl
                        self.active_block.move(event.pos)
            if event.button == 3:
                for bl in self.blocks:
                    if bl.is_colliding(event.pos):
                        self.blocks.remove(bl)
        elif event.type == pg.MOUSEBUTTONUP:
            if self.active_block != None:
                self.active_block.drop()
                #self.recalculate(self.old_block_range)
                #self.recalculate((self.active_block.t,self.active_block.get_end_time()))
                self.active_block = None
            

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.buttons["load_button"]):
            self.file_dialog = UIFileDialog(pg.Rect(160, 50, 440, 500),
                                            self.parent.ui_manager,
                                            window_title='Load File',
                                            # initial_file_path='',
                                            # allow_picking_directories=True,
                                            allow_existing_files_only=True,
                                            allowed_suffixes={".wav"})
            self.buttons["load_button"].disable()
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.buttons["play_sound_button"]):
            max_time = 0
            for b in self.blocks:
                max_time = b.get_end_time()
            self.recalculate((0,max_time))
            sd.play(self.sound/play_midi.INT16_LIMIT, self.sample_rate) #uses values between -1.0 and 1.0
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.buttons["stop_sound_button"]):
            sd.stop()
        
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.buttons["export_wav_button"]):
            max_time = 0
            for b in self.blocks:
                max_time = b.get_end_time()
            self.recalculate((0,max_time))
            write_wav(path="wavy.wav",wav_rate=self.sample_rate,np_array=self.sound.astype(np.short))
        
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.buttons["midi_block_button"]):
            self.blocks = [Block(self,self.parent.get_midi_block(),sample_rate=44100,t=0,ch=1,text = "Midi"+str(len(self.blocks)))] + self.blocks
            #self.recalculate((0,self.blocks[0].get_end_time()))
        
        if (event.type == pygame_gui.UI_WINDOW_CLOSE
                    and event.ui_element == self.file_dialog):
                self.buttons["load_button"].enable()
                self.file_dialog = None
        
        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            _,ending = event.text.split(".")
            if ending == "wav":
                rate,data = read_wav(event.text)
                self.blocks = [Block(self,data,sample_rate=rate,t=0,ch=1,text = "Wav"+str(len(self.blocks)))] + self.blocks
                #self.recalculate((0,self.blocks[0].get_end_time()))


class Block():#should be able to store midi, wav and custom music sections
    def __init__(self, parent, data = np.array([]),sample_rate=44100,t=0,ch=0, text = ""):
        self.parent = parent #assume it's always arangementTabBody()
        self.data = data
        self.sample_rate = sample_rate
        self.t=t
        self.ch=ch
        self.text = text
        
        self.effected = data
    
    def get_end_time(self):
        return self.t + self.data.shape[0]/self.sample_rate 
    
    def apply_effects(self, effects):
        self.effected = effects(data) #TODO
    
    def render(self,screen):
        px_per_sec = round(RECT_WIDTH/TIMELINE_LENGTH)
        x = self.t * px_per_sec + self.parent.absolute_offset[0]
        y = (self.ch-1) * CHANNEL_HEIGHT + self.parent.absolute_offset[1]
        w = (self.data.shape[0]/self.sample_rate)*(RECT_WIDTH/TIMELINE_LENGTH) + min(x,0) + min(RECT_WIDTH-RECT_X_OFFSET-x,0)
        h = CHANNEL_HEIGHT + min(y,0) + min(RECT_HEIGHT-RECT_Y_OFFSET-y,0)
        rect = pg.Rect(max(x,0)+ RECT_X_OFFSET,max(y,0) + RECT_Y_OFFSET,min(max(w,0),RECT_WIDTH),h)
        pg.draw.rect(screen, pg.Color("cadetblue"), rect, width=0)
        if pg.font:
                font = pg.font.Font(None, 32)
                name = font.render(self.text, True, (0, 0, 0))
                screen.blit(name,name.get_rect(center = rect.center))
    
    def move(self, mouse_pos):
        px_per_sec = round(RECT_WIDTH/TIMELINE_LENGTH)
        pos = list(mouse_pos)
        #clamp the movement
        if pos[0] < RECT_X_OFFSET:
            pos[0] = RECT_X_OFFSET
        elif pos[0] > RECT_X_OFFSET+RECT_WIDTH:
            pos[0] = RECT_X_OFFSET+RECT_WIDTH
        if pos[1] < RECT_Y_OFFSET:
            pos[1] = RECT_Y_OFFSET
        elif pos[1] > RECT_Y_OFFSET+RECT_HEIGHT:
            pos[1] = RECT_Y_OFFSET+RECT_HEIGHT
        
        self.t = (pos[0]-self.parent.absolute_offset[0] - RECT_X_OFFSET)/px_per_sec
        self.ch = (pos[1]-self.parent.absolute_offset[1] - RECT_Y_OFFSET)/CHANNEL_HEIGHT + 1
    
    def drop(self):#snap to nearest channel when dropped
        self.ch = round(self.ch)
    
    def is_colliding(self, pos):
        px_per_sec = round(RECT_WIDTH/TIMELINE_LENGTH)
        x = self.t * px_per_sec + self.parent.absolute_offset[0]
        y = (self.ch-1) * CHANNEL_HEIGHT + self.parent.absolute_offset[1]
        w = (self.data.shape[0]/self.sample_rate)*(RECT_WIDTH/TIMELINE_LENGTH)
        h = CHANNEL_HEIGHT
        rect = pg.Rect(max(x,0) + RECT_X_OFFSET,max(y,0) + RECT_Y_OFFSET,w,h)
        return rect.collidepoint(pos)
