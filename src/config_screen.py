import tkinter as tk
import global_variables as gv
from tkinter_componets.add_alert_time_component import Add_Alert_Time_Component
from stop_watch_overlay import Stop_Watch_Overlay

class Config_Screen:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Configurar Temporizador")

        tk.Label(self.root, text="Minutos:").pack()
        self.entry_minutes = tk.Entry(self.root)
        self.entry_minutes.pack()

        tk.Label(self.root, text="Segundos:").pack()
        self.entry_seconds = tk.Entry(self.root)
        self.entry_seconds.pack()

        alerts_frame = tk.Frame(self.root)
        alerts_frame.pack()

        tk.Button(self.root, 
                  text="Agregar Alerta", 
                  command=lambda: Add_Alert_Time_Component(alerts_frame)).pack()
        
        tk.Button(self.root, text="Iniciar", command=lambda: self.start_timer()).pack()
        self.root.mainloop()

    def start_timer(self):

        minutes = int(self.entry_minutes.get()) if self.entry_minutes.get().isdigit() else 0
        seconds = int(self.entry_seconds.get()) if self.entry_seconds.get().isdigit() else 0
        gv.time_remaining = minutes * 60 + seconds
        gv.original_time = gv.time_remaining
        gv.alert_times.clear()
        for entriy in gv.alert_entries:
            min_val = int(entriy["min"].get()) if entriy["min"].get().isdigit() else 0
            sec_val = int(entriy["sec"].get()) if entriy["sec"].get().isdigit() else 0
            gv.alert_times.append(min_val * 60 + sec_val)
         
        self.root.destroy()
        Stop_Watch_Overlay()
