import pytchat
import pyttsx3
import time
import gc
import threading
import tkinter
import requests

# idk

#config
VIDEO_ID = "atFv0M3Df2Y"
VIDEO_WEBHOOK_PATH = f"{__file__}/../DISCORD_VIDEO_WEBHOOK.txt"
COMMAND_CHAR = "/"
PING = "<@&1431111239278264392>"
MAX_MESSAGE_LENGH = 300

DEBUG = False

file = open(VIDEO_WEBHOOK_PATH, "r")
VIDEO_WEBHOOK = file.read()
file.close()

# default message format — you can edit this in the window
message_format = "{c.author.name} says {c.message}"

window = None
chat = None
volume = 1
speed = 170

"""
def worker():
    print("Worker starting")
    time.sleep(2)
    print("Worker done")

t = threading.Thread(target=worker)
t.start()
t.join()
"""

"""
while chat.is_alive():
        for c in chat.get().sync_items():
            text = f"{c.author.name} says {c.message}"
            print(text)

            # 🔧 Initialize engine fresh each loop
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.setProperty('volume', 1.0)

            engine.say(text)
            engine.runAndWait()

            # ✅ Properly stop engine and release COM resources
            engine.stop()
            del engine
            gc.collect()

        time.sleep(1)
"""

def pingForVideo(id):
    global VIDEO_WEBHOOK, PING
    requests.post(VIDEO_WEBHOOK)
    data = {
        "content": f"{PING}\nhttps://www.youtube.com/watch?v={id}",
        "username": "TTS"  # optional: change the username
    }
    response = requests.post(VIDEO_WEBHOOK, json=data)

def readChat():
    global message_format, volume, speed, DEBUG, COMMAND_CHAR, MAX_MESSAGE_LENGH
    for c in chat.get().sync_items():
        try:
            if c.message.startswith(COMMAND_CHAR): continue
            
            # safely evaluate the format using f-string style substitution
            text = eval(f"f'''{message_format}'''", {"c": c})
            if len(text) > MAX_MESSAGE_LENGH:
                text = f"shut up {c.author.name}"
        except Exception as e:
            text = f"[FORMAT ERROR: {e}]"
        print(text)

        # 🔧 Initialize engine fresh each loop
        engine = pyttsx3.init()
        #engine.setProperty("")
        print(speed)
        print(volume)
        engine.setProperty('rate', float(speed))
        engine.setProperty('volume', float(volume))

        engine.say(text)
        engine.runAndWait()

        # ✅ Properly stop engine and release COM resources
        engine.stop()
        del engine
        gc.collect()

def readChatLoop():
    while chat.is_alive():
        readChat()
        time.sleep(1)

def message_format_box_event_on_text_change(*args):
    global message_format, DEBUG
    text = text_var.get()
    if DEBUG:
        print("Current text:", text)
    message_format = text

def vol_slider_event_on_change(value):
    global volume, DEBUG
    if DEBUG:
        print("Volume:", value)
    volume = value

def speed_slider_event_on_change(value):
    global speed, DEBUG
    if DEBUG:
        print("Speed:", value)
    speed = value

if not DEBUG:
    while True:
        try:
            chat = pytchat.create(video_id=VIDEO_ID)
            print("Connected to live chat...")

            if chat != None:
                pingForVideo(VIDEO_ID)
            
            window = tkinter.Tk("TTS")

            # Make text variable and entry box
            text_var = tkinter.StringVar(value=message_format)
            text_var.trace("w", message_format_box_event_on_text_change)  # runs whenever text changes

            entry = tkinter.Entry(window, textvariable=text_var, width=80)
            entry.pack(padx=10, pady=10)

            # Create a slider (Scale widget)
            volume_slider = tkinter.Scale(
                window,
                from_=0,          # minimum value
                to=2,           # maximum value
                resolution=0.1,
                orient="horizontal",  # make it go left→right
                label="Volume",   # text shown above it
                command=vol_slider_event_on_change  # function to run when moved
            )
            volume_slider.set(volume)  # starting value
            volume_slider.pack(padx=10, pady=10)

            speed_slider = tkinter.Scale(
                window,
                from_=0,          # minimum value
                to=170*2,           # maximum value
                #resolution=0.1,
                orient="horizontal",  # make it go left→right
                label="Speed",   # text shown above it
                command=speed_slider_event_on_change  # function to run when moved
            )
            speed_slider.set(speed)  # starting value
            speed_slider.pack(padx=10, pady=10)

            #button = tkinter.Button(window, text="click", function=)
            #button.pack()

            print("window setup finished")
            print("starting tts")
            t = threading.Thread(target=readChatLoop)
            t.start()
            print("tts started")
            #t.join()
            window.mainloop()
            print("end")


        except KeyboardInterrupt:
            print("\nStopped by user.")
else:
    pingForVideo("X4VjzN8Z7Bw")