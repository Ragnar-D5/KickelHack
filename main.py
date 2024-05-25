from io_functions import read_midi,read_wav,debug_play_np_array
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path


class Mainwindow:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Basic Synthesizer')
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

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()

if __name__ == "__main__":
    print(read_midi("test_files/TOUHOU_-_Bad_Apple.mid").instruments)
    rate,data = read_wav("test_files/never_gonna_test.wav")
    # debug_play_np_array(data,rate)

    window_surface = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    print(window_surface.get_rect())
    app = Mainwindow()
    app.run()
