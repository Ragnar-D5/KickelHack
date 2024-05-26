import pygame as pg
from io_functions import read_midi
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog

class ArangementTabBody():
    def __init__(self, parent):
        self.parent = parent
        
        self.sample_rate = 44100
        
        #the place where everything is stored
        self.sound = np_array([])
        
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
                                             'bottom': 'bottom'})
        }
        self.file_dialog = None
    
    def hide_buttons(self):
        for btn in self.buttons.values():
            btn.visible = False
    def unhide_buttons(self):
        for btn in self.buttons.values():
            btn.visible = True    
    
    def ui(self,screen):
        pass

    def event(self, event):
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.buttons["load_button"]):
            self.file_dialog = UIFileDialog(pg.Rect(160, 50, 440, 500),
                                            self.parent.ui_manager,
                                            window_title='Load File',
                                            # initial_file_path='',
                                            # allow_picking_directories=True,
                                            allow_existing_files_only=True,
                                            allowed_suffixes={".wav",".mid"})
            self.buttons["load_button"].disable()
        
        if (event.type == pygame_gui.UI_WINDOW_CLOSE
                    and event.ui_element == self.file_dialog):
                self.buttons["load_button"].enable()
                self.file_dialog = None
        
        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                if self.display_loaded_image is not None:
                    self.display_loaded_image.kill()
