import pygame
import ctypes
import sys
import win32gui
import win32con
import tkinter as tk
import threading as thr

pygame.mixer.init()
time_remaining = 0  # Tiempo en segundos
original_time = 0  # Guardar el tiempo original para reiniciar
alert_times = []  # Lista de tiempos en los que cambiará a rojo

def run_timmer():
    timer_thread = thr.Thread(target=update_timer, daemon=True)
    timer_thread.start()

def play_alert_sound():
    print("Deberia sonar")
    pygame.mixer.Sound("src/audio/snap--out---of--it.mp3").play()

def update_timer():
    global time_remaining
    while time_remaining > 0:
        pygame.time.delay(1000)
        time_remaining -= 1
        if time_remaining in alert_times:
            play_alert_sound()

def format_time(seconds):
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes:02}:{sec:02}"

def set_background_window(WIDTH, HEIGHT):
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Temporizador Transparente")
    return screen

def stopwatch_overlay():
    global time_remaining, original_time
    pygame.init()
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = set_background_window(WIDTH, HEIGHT)
    TRANSPARENT_COLOR = (0,0,0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GRAY = (50, 50, 50, 180)  # Gris semitransparente
    FONT = pygame.font.Font(None, 80)
    ICON_FONT = pygame.font.Font(None, 40)
    
    if sys.platform == "win32":
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, WIDTH, HEIGHT, 0)
        WS_EX_LAYERED = 0x00080000
        GWL_EXSTYLE = -20
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE) | WS_EX_LAYERED)
        def RGB(r, g, b):
            return (r & 0xFF) | ((g & 0xFF) << 8) | ((b & 0xFF) << 16)
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, RGB(*TRANSPARENT_COLOR), 0, 1)
    
    clock = pygame.time.Clock()
    timer_thread = thr.Thread(target=update_timer, daemon=True)
    timer_thread.start()
    
    # Posiciones
    TIMER_RECT = pygame.Rect(WIDTH // 2 - 150, HEIGHT * 3 // 4 - 50, 300, 100)
    RESET_BUTTON_RECT = pygame.Rect(WIDTH // 2 - 40, HEIGHT * 3 // 4 + 80, 80, 40)

    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if RESET_BUTTON_RECT.collidepoint(event.pos):  # Si el clic está dentro del botón
                    time_remaining = original_time  # Reiniciar el temporizador
                    run_timmer()
        
        screen.fill(TRANSPARENT_COLOR)
        
        # Dibujar fondo del temporizador
        pygame.draw.rect(screen, (50, 50, 50, 180), TIMER_RECT, border_radius=15)
        
        # Cambiar color si es tiempo de alerta
        text_color = RED if time_remaining in alert_times else WHITE
        time_text = FONT.render(format_time(time_remaining), True, text_color)
        text_rect = time_text.get_rect(center=TIMER_RECT.center)
        screen.blit(time_text, text_rect)
        
        # Dibujar botón de reinicio
        pygame.draw.rect(screen, RED, RESET_BUTTON_RECT, border_radius=10)
        reset_text = ICON_FONT.render("R", True, WHITE)
        reset_rect = reset_text.get_rect(center=RESET_BUTTON_RECT.center)
        screen.blit(reset_text, reset_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

def get_timer_duration():
    global time_remaining, original_time, alert_times
    root = tk.Tk()
    root.title("Configurar Temporizador")
    
    tk.Label(root, text="Minutos:").pack()
    entry_minutes = tk.Entry(root)
    entry_minutes.pack()
    
    tk.Label(root, text="Segundos:").pack()
    entry_seconds = tk.Entry(root)
    entry_seconds.pack()
    
    alert_entries = []
    
    def add_alert_time():
        frame = tk.Frame(root)
        tk.Label(frame, text="Min:").pack(side=tk.LEFT)
        entry_alert_min = tk.Entry(frame, width=5)
        entry_alert_min.pack(side=tk.LEFT)
        tk.Label(frame, text="Sec:").pack(side=tk.LEFT)
        entry_alert_sec = tk.Entry(frame, width=5)
        entry_alert_sec.pack(side=tk.LEFT)
        alert_entries.append((entry_alert_min, entry_alert_sec))
        frame.pack()
    
    tk.Button(root, text="Agregar Alerta", command=add_alert_time).pack()
    
    def start_timer():
        global time_remaining, original_time, alert_times
        minutes = int(entry_minutes.get()) if entry_minutes.get().isdigit() else 0
        seconds = int(entry_seconds.get()) if entry_seconds.get().isdigit() else 0
        time_remaining = minutes * 60 + seconds
        original_time = time_remaining  # Guardar tiempo original
        alert_times.clear()
        for min_entry, sec_entry in alert_entries:
            min_val = int(min_entry.get()) if min_entry.get().isdigit() else 0
            sec_val = int(sec_entry.get()) if sec_entry.get().isdigit() else 0
            alert_times.append(min_val * 60 + sec_val)
        root.destroy()
        stopwatch_overlay()
    
    tk.Button(root, text="Iniciar", command=start_timer).pack()
    root.mainloop()

if __name__ == "__main__":
    get_timer_duration()
