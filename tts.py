import pytchat
import pyttsx3
import time
import gc
import threading
import tkinter
import requests
import re

# ---------------------------
# Video ID lookup (new)
def get_channel_id_from_handle(handle):
    """Resolve a YouTube handle (@CosmoTed) to channel ID."""
    url = f"https://www.youtube.com/{handle}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    m = re.search(r'<link rel="canonical" href="https://www.youtube.com/channel/(UC[\w-]+)">', r.text)
    if m:
        return m.group(1)
    return None

def get_live_video_id(channel_id):
    """Check if the channel has a live video; returns video ID if live."""
    url = f"https://www.youtube.com/channel/{channel_id}/live"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, allow_redirects=True)
    if "watch?v=" in r.url:
        return r.url.split("v=")[-1].split("&")[0]
    return None

# ---------------------------
#config
handle = "@TylerBednarik"  # Replace with target handle
channel_id = get_channel_id_from_handle(handle)

if not channel_id:
    print("Could not resolve channel")
    VIDEO_ID = None
else:
    VIDEO_ID = get_live_video_id(channel_id)
    if not VIDEO_ID:
        print("No live stream currently")
    else:
        print("Using live video ID:", VIDEO_ID)

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

# ---------------------------
# rest of your code remains unchanged
def pingForVideo(id):
    global VIDEO_WEBHOOK, PING
    requests.post(VIDEO_WEBHOOK)
    data = {
        "content": f"{PING}\nhttps://www.youtube.com/watch?v={id}",
        "username": "TTS"
    }
    response = requests.post(VIDEO_WEBHOOK, json=data)

# ... rest of your functions: readChat(), readChatLoop(), slider events, etc.

if not DEBUG:
    while True:
        try:
            if VIDEO_ID is None:
                time.sleep(10)
                continue  # wait until a live stream is available

            chat = pytchat.create(video_id=VIDEO_ID)
            print("Connected to live chat...")

            if chat is not None:
                pingForVideo(VIDEO_ID)

            window = tkinter.Tk()
            window.title("TTS")

            # Make text variable and entry box
            text_var = tkinter.StringVar(value=message_format)
            text_var.trace("w", message_format_box_event_on_text_change)

            entry = tkinter.Entry(window, textvariable=text_var, width=80)
            entry.pack(padx=10, pady=10)

            # Volume slider
            volume_slider = tkinter.Scale(
                window, from_=0, to=2, resolution=0.1, orient="horizontal",
                label="Volume", command=vol_slider_event_on_change
            )
            volume_slider.set(volume)
            volume_slider.pack(padx=10, pady=10)

            # Speed slider
            speed_slider = tkinter.Scale(
                window, from_=0, to=340, orient="horizontal",
                label="Speed", command=speed_slider_event_on_change
            )
            speed_slider.set(speed)
            speed_slider.pack(padx=10, pady=10)

            print("window setup finished")
            print("starting tts")
            t = threading.Thread(target=readChatLoop)
            t.start()
            print("tts started")

            window.mainloop()
            print("end")

        except KeyboardInterrupt:
            print("\nStopped by user.")
else:
    pingForVideo("X4VjzN8Z7Bw")

