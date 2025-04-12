import tkinter as tk
import global_variables as gv

class Add_Alert_Time_Component:

    def __init__(
              self,
              container
              ):
        self.frame = tk.Frame(container)
        tk.Label(self.frame, text="Min:").pack(side=tk.LEFT)
        entry_alert_min = tk.Entry(self.frame, width=5)
        entry_alert_min.pack(side=tk.LEFT)
        tk.Label(self.frame, text="Sec:").pack(side=tk.LEFT)
        entry_alert_sec = tk.Entry(self.frame, width=5)
        entry_alert_sec.pack(side=tk.LEFT)
        self.entries = {"min": entry_alert_min, "sec": entry_alert_sec}
        gv.alert_entries.append(self.entries)
        delete_alert_button = tk.Button(self.frame, text= "x", command= lambda: self.delete_alert())
        delete_alert_button.pack()
        self.frame.pack()
        

    def delete_alert(self):
        gv.alert_entries.remove(self.entries)
        self.frame.destroy()
