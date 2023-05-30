import cv2
import numpy as np
import pyaudio
import wave
import datetime
import pyautogui


#set up audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

frames = []


#set the video recording
SCREEN_SIZE = (1920, 1080)
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, SCREEN_SIZE)


def record():
    # Record screen and audio
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < RECORD_SECONDS:
        # Record audio
        data = stream.read(CHUNK)
        frames.append(data)

        # Record video
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

def stop():
    # stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    out.release()

    # Save audio recording
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


record()
stop()