import pygame
import global_variables as gv
import threading as thr


def play_alert_sound():
    print("Debería sonar")
    pygame.mixer.Sound("src/audio/snap--out---of--it.mp3").play()

def update_timer():
    print("[HILO] Iniciando nuevo hilo")
    while True:
        pygame.time.delay(1000)
        gv.time_remaining -= 1
        print(f"[HILO] Tiempo restante: {gv.time_remaining}")
        if gv.time_remaining in gv.alert_times:
            play_alert_sound()
            

def run():
    timer_thread = thr.Thread(target=update_timer, daemon=True)
    timer_thread.start()

def format_time(seconds):
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes:02}:{sec:02}"
