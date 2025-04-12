import pygame
import sys
import win32gui
import win32con
import ctypes
import global_variables as gv
import timer

class Stop_Watch_Overlay:

    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h
        screen = self.set_background_window()
        TRANSPARENT_COLOR = (0,0,0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        FONT = pygame.font.Font(None, 80)
        ICON_FONT = pygame.font.Font(None, 40)
        
        if sys.platform == "win32":
            hwnd = pygame.display.get_wm_info()["window"]
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, self.WIDTH, self.HEIGHT, 0)
            WS_EX_LAYERED = 0x00080000
            GWL_EXSTYLE = -20
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE) | WS_EX_LAYERED)
            def RGB(r, g, b):
                return (r & 0xFF) | ((g & 0xFF) << 8) | ((b & 0xFF) << 16)
            ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, RGB(*TRANSPARENT_COLOR), 0, 1)
        
        clock = pygame.time.Clock()
        timer.run()

        TIMER_RECT = pygame.Rect(self.WIDTH // 2 - 150, self.HEIGHT * 3 // 4 - 50, 300, 100)
        RESET_BUTTON_RECT = pygame.Rect(self.WIDTH // 2 - 40, self.HEIGHT * 3 // 4 + 80, 80, 40)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if RESET_BUTTON_RECT.collidepoint(event.pos):
                        timer.reset()
            
            screen.fill(TRANSPARENT_COLOR)

            pygame.draw.rect(screen, (50, 50, 50, 180), TIMER_RECT, border_radius=15)

            text_color = RED if gv.time_remaining in gv.alert_times else WHITE
            time_text = FONT.render(timer.format_time(gv.time_remaining), True, text_color)
            text_rect = time_text.get_rect(center=TIMER_RECT.center)
            screen.blit(time_text, text_rect)

            pygame.draw.rect(screen, RED, RESET_BUTTON_RECT, border_radius=10)
            reset_text = ICON_FONT.render("R", True, WHITE)
            reset_rect = reset_text.get_rect(center=RESET_BUTTON_RECT.center)
            screen.blit(reset_text, reset_rect)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()
    
    def set_background_window(self):
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.NOFRAME)
        pygame.display.set_caption("Temporizador Transparente")
        return screen
