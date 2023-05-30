"""
PYMyScreenRecorder
Version : 1.0
Description : This is a GUI based screen recorrder written in python.It will record whole screen window.
              initially it has record,pause and stop button.It will generate an .avi video file and a .wav
              audio file in output directory.

Build Date : 30th May, 2023
Developer : Bapon Kar
License : GNU GPL v3.0
Download : https://github.com/baponkar
Credit : chatGPT, stackoverflow.com
contact : gamingjam60@gmail.com
"""


#imported modules
import tkinter as tk
import cv2
import numpy as np
import pyaudio
import wave
import datetime
import pyautogui

import threading
import os
from tkinter.ttk import *
from tkinter import *
from PIL import Image, ImageTk


root = tk.Tk()
root.configure(bg='grey')

#getting screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


#set up directory
current_dir = str(os.getcwd())
output_dir = current_dir + "\\output\\"
icons_dir = str(current_dir) + "\\icons\\"
pause_circle = str(icons_dir + "pause_circle.png")
play_circle = str(icons_dir + "play_circle.png")
stop_circle = str(icons_dir + "stop_circle.png")
recorder_icon = str(icons_dir + "screen_recorder.png")



# Creating a photoimage object to use image
start_photo = PhotoImage(file = play_circle)
pause_photo = PhotoImage(file = pause_circle)
stop_photo = PhotoImage(file = stop_circle)
screen_recorder_icon = PhotoImage(file = recorder_icon)


#setting root
root.iconphoto(True, screen_recorder_icon)
#root.iconbitmap(recorder_icon)

#Recording Control
RECORD_START = False
RECORD_PAUSE = False
RECORD_STOP = True

RECORDING_START_TIME = datetime.datetime.now()
RECORDING_TIME = 0
RECORDING_STOP_TIME = 0
RECORDING_TIME_LIMIT = 0 #milli seconds


#set up audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = output_dir  + str(RECORDING_START_TIME.year) + "-" +  str(RECORDING_START_TIME.month) + "-" +  str(RECORDING_START_TIME.day) + "-" + str(RECORDING_START_TIME.hour) + "-" +  str(RECORDING_START_TIME.minute) + "-" +  str(RECORDING_START_TIME.second) + "-" + "output.wav"

audio = pyaudio.PyAudio()

audio_stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

frames = []


#set the video recording

SCREEN_SIZE = (screen_width,screen_height) #get window size
fourcc = cv2.VideoWriter_fourcc(*"XVID")
AVI_OUTPUT_FILENAME = output_dir  + str(RECORDING_START_TIME.year) + "-" +  str(RECORDING_START_TIME.month) + "-" +  str(RECORDING_START_TIME.day) + "-" + str(RECORDING_START_TIME.hour) + "-" +  str(RECORDING_START_TIME.minute) + "-" +  str(RECORDING_START_TIME.second) + "-"  + "output.avi"
vid_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME, fourcc, 20.0, SCREEN_SIZE)


def record():
    RECORD_START = True
    # Record screen and audio
    RECORDING_START_TIME = datetime.datetime.now()


    if RECORDING_TIME_LIMIT == 0:
        while RECORD_START == True:
            RECORDING_TIME = (datetime.datetime.now() -  RECORDING_START_TIME).seconds
            # Record audio
            data = audio_stream.read(CHUNK)
            frames.append(data)


            # Record video
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            vid_out.write(frame)
    else:
        while RECORD_START == True and (datetime.datetime.now() - RECORDING_START_TIME).seconds < RECORDING_TIME_LIMIT:
            RECORDING_TIME = (datetime.datetime.now() -  RECORDING_START_TIME).seconds

            # Record audio
            data = audio_stream.read(CHUNK)
            frames.append(data)

            # Record video
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            vid_out.write(frame)

def stop():
    RECORD_START = False
    RECORD_STOP = True
    # stop recording
    audio_stream.stop_stream()
    audio_stream.close()
    audio.terminate()

    vid_out.release()

    # Save audio recording
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
#-------------------------------------------------------------------------------------------

WINDOW_HEIGHT = 50
WINDOW_WIDTH = 500

class ScreenRecorderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Screen Recorder")

        # Create play, pause, and stop buttons
        self.play_button = tk.Button(master, text="Record" , command=self.record_start, width=50, height=50, bg='green',fg='white', image=start_photo)
        self.pause_button = tk.Button(master, text="Pause", command=self.record_pause, width=50, height=50, image=pause_photo)
        self.pause_button["state"] = "disabled"
        self.stop_button = tk.Button(master, text="Stop", command=self.record_stop, width=50, height=50, bg='red',fg='white', image = stop_photo)
        self.stop_button["state"] = "disabled"

        # Create a label to display the current stage of screen recording
        self.stage_label = tk.Label(master, text="Not recording", bg='grey',padx=5,fg='white')

        # Pack buttons and label into the GUI
        self.play_button.pack(side="left", padx=5, pady=5)
        self.pause_button.pack(side="left",padx=5, pady=5)
        self.stop_button.pack(side="left",padx=5, pady=5)
        self.stage_label.pack(side="bottom", padx=2, pady=5)

    def record_start(self):
        self.play_button["state"] = "disabled"
        self.pause_button["state"] = "normal"
        self.stop_button["state"] = "normal"

        # Change stage label to "Recording"
        self.stage_label.config(text="Recording started...")
        threading.Thread(target=record, daemon=True).start()

    def record_pause(self):
        # Change stage label to "Paused"
        self.stage_label.config(text="Recording Paused")

    def record_stop(self):
        self.pause_button["state"] = "disabled"
        self.stop_button["state"] = "disabled"
        # Change stage label to "Stopped"
        self.stage_label.config(text="Recording stopped")
        stop()
        cv2.destroyAllWindows()
        root.destroy
        


root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
my_gui = ScreenRecorderGUI(root)
root.mainloop()



