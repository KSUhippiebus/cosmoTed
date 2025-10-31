import minescript
import chatApi

video_id = "iw45r7BU2jc"
command_char = "/"

DEBUG = True

checkPointX = 0
checkPointY = 70
checkPointZ = 0

def onMessage(message):
    global checkPointX, checkPointY, checkPointZ  # needed for updates
    content = message.message.strip()
    #print(content)

    # only process messages that start with "/"
    if not content.startswith(command_char):
        return

    parts = content[1:].split()  # remove "/" then split by spaces
    if len(parts) == 0:
        return

    cmd = parts[0].lower()
    args = parts[1:]
    #print(args)

    #print(f"Command: {cmd}, Args: {args}")

    # handle commands safely
    if cmd == "summon":
        if len(args) < 1:
            minescript.echo("Usage: /summon <mob>")
            return
        print(f"/summon minecraft:{args[0]}")

    elif cmd == "fill":
        if len(args) < 1:
            minescript.echo("Usage: /fill <block>")
            return
        minescript.echo(f"/fill ~-10 ~-10 ~-10 ~10 ~10 ~10 minecraft:{args[0]}")
        print(f"/fill ~-10 ~-10 ~-10 ~10 ~10 ~10 minecraft:{args[0]}")
        print("/fill ~1 ~1 ~1 ~-1 ~-1 ~-1 air")

    elif cmd == "checkpoint":
        checkPointX = minescript.player.x
        checkPointY = minescript.player.y
        checkPointZ = minescript.player.z
        minescript.echo(f"Checkpoint set at {checkPointX}, {checkPointY}, {checkPointZ}")

    elif cmd == "return":
        print(f"/tp {checkPointX} {checkPointY} {checkPointZ}")
        minescript.echo(f"Teleported to checkpoint: {checkPointX}, {checkPointY}, {checkPointZ}")
    
    elif cmd == "sound":
        if len(args) > 0:
            print(f"/playsound {args[0]} hostile @s ^ ^ ^-3 1 0.5")
        else:
            print(f"/playsound entity.creeper.primed hostile @s ^ ^ ^-3 1 0.5")
    
    elif cmd == "potion":
        print(f"/effect give @s {args[0]} 10")


    elif cmd == "command":
        commandText = ' '.join(args)
        if not DEBUG and message.author.name.lower() == "ksuhippiebus":
            print(commandText)
        elif DEBUG:
            print(commandText)

    elif cmd == "cannon":
        for y in range(-55,200):
            print(f"/summon tnt ~ {y} ~ "+"{NoGravity:1b,fuse:100}")

    else:
        minescript.echo(f"Unknown command: /{cmd}")

    if DEBUG:
        raise KeyboardInterrupt

if DEBUG:
    #chatApi.debug_connect("/command /tellraw @s {\"text\":\"test\"}", onMessage)
    chatApi.debug_connect("/cannon", onMessage)
else:
    chatApi.connect(video_id, onMessage)
