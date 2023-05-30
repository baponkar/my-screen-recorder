import tkinter as tk

window_height = 300
window_width = 500

class ScreenRecorderGUI:

    def __init__(self, master):
        self.master = master
        master.title("Screen Recorder")

        # Create play, pause, and stop buttons
        self.play_button = tk.Button(master, text="Record", command=self.record_start, width=10, height=2)
        
        self.pause_button = tk.Button(master, text="Pause", command=self.record_pause, width=10, height=2)
        self.stop_button = tk.Button(master, text="Stop", command=self.record_stop, width=10, height=2)

        # Create a label to display the current stage of screen recording
        self.stage_label = tk.Label(master, text="Not recording")

        # Pack buttons and label into the GUI
        self.play_button.pack()
        self.pause_button.pack()
        self.stop_button.pack()
        self.stage_label.pack()

    def record_start(self):
        # Change stage label to "Recording"
        self.stage_label.config(text="Recording")

    def record_pause(self):
        # Change stage label to "Paused"
        self.stage_label.config(text="Recording Paused")

    def record_stop(self):
        # Change stage label to "Stopped"
        self.stage_label.config(text="Recording Stopped")

root = tk.Tk()
root.geometry(str(window_width) + "x" + str(window_height))
my_gui = ScreenRecorderGUI(root)
root.mainloop()
