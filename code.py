import board
import digitalio
import time
import neopixel

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10,brightness=0.05)
Red = (100,0,0)
Orange = (100,40,0)
Green = (0,100,0)
#pixels[0] = Green
pomo = 0
tik = 0
pixels[pomo] = (0, 0, 30)


# Enable the speaker
spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True
 
# Make the 2 input buttons
buttonA = digitalio.DigitalInOut(board.D4)
buttonA.direction = digitalio.Direction.INPUT
buttonA.pull = digitalio.Pull.DOWN

buttonB = digitalio.DigitalInOut(board.D5)
buttonB.direction = digitalio.Direction.INPUT
buttonB.pull = digitalio.Pull.DOWN

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

def play_file(filename):
    print("Playing file: " + filename)
    wave_file = open(filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                pass
    print("Finished")

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def rainbow(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)


def addPomo():
    if buttonB.value and buttonA.value:
        return True
    else:
        return False

while pomo<10:
    if tik>=0:
        pixels[pomo] = (0, 0, 30)
    if tik>1800:
        play_file("clock.wav")
        tik = 0
    else:
        tik+=1
        time.sleep(0.5)
    
    if buttonB.value:
        time.sleep(0.5)
        if addPomo():
            play_file("coin.wav")
            pixels[pomo] = (100, 0, 0)
            pomo+=1
            tik = 0
            pixels[pomo] = (0, 0, 30)
            time.sleep(3)
            continue
        tik = -1800
        pixels[pomo] = (0, 0, 0)
    
    if buttonA.value:
        time.sleep(0.5)
        if addPomo():
            play_file("coin.wav")
            pixels[pomo] = (100, 0, 0)
            pomo+=1
            tik = 0
            pixels[pomo] = (0, 0, 30)
            time.sleep(3)
            continue
        pomo_g = 100
        pomo_r = 0
        pixels[pomo] = (pomo_r, pomo_g, 0)
        for i in range(0,50):
            time.sleep(30)
            pomo_g -=1
            pomo_r +=1
            pixels[pomo] = (pomo_r, pomo_g, 0)
        pixels[pomo] = (100, 0, 0)
        play_file("coin.wav")
        pomo +=1
        if pomo == 10:
            break
        tik = 0
        pixels[pomo] = (0, 0, 30)

while 1:
    rainbow_cycle(0.05)
