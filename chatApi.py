import pytchat

DEBUG = False

chat = None

def connect(videoId, handleMessage):
    chat = pytchat.create(video_id=videoId)
    while True:
        for c in chat.get().sync_items():
            handleMessage(c)

class debugMessage:
    def __init__(self,message):
        self.message = message

def debug_connect(testMessage,handleMessage):
    message = debugMessage(testMessage)
    while True:
        handleMessage(message)