import pygame
import global_variables as gv
import threading as thr
import traceback

def play_alert_sound():
    print("Debería sonar")
    pygame.mixer.Sound("src/audio/snap--out---of--it.mp3").play()

def update_timer():
    try:
        gv.contador_hilos += 1
        id_hilo = gv.contador_hilos
        print(f"[HILO{id_hilo}] Iniciando nuevo hilo")
        while not (gv.stop_timer_event.is_set() or gv.time_remaining < 0) :
            pygame.time.delay(1000)
            gv.time_remaining -= 1
            print(f"[HILO{id_hilo}] Tiempo restante: {gv.time_remaining}")
            if gv.time_remaining in gv.alert_times:
                play_alert_sound()
        print(f"[HILO{id_hilo}] Terminado")
        gv.timer_runing_event.clear()
    except Exception as e:
        print("error:")
        traceback.print_exc()
            

def run():
    gv.stop_timer_event.clear()
    while True:
        if not gv.timer_runing_event.is_set():
            timer_thread = thr.Thread(target=update_timer, daemon=True)
            timer_thread.start()
            gv.timer_runing_event.set()
            break
        else:
            pygame.time.delay(50)

def format_time(seconds):
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes:02}:{sec:02}"

def reset():
    print("[MAIN] Reiniciando temporizador")
    gv.stop_timer_event.set()
    while gv.timer_runing_event.is_set():
        pygame.time.delay(50)
    gv.time_remaining = gv.original_time
    run()
