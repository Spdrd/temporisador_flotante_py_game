import threading as thr

time_remaining = 0
original_time = 0
alert_times = []
alert_entries = []
stop_timer_event = thr.Event()
stop_timer_event.clear()
timer_runing_event = thr.Event()
timer_runing_event.clear()
contador_hilos = 0