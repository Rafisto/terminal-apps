import os
import cv2
import numpy
import atexit
import time
from parameters import ArgumentParser

pixel_set = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
play_color = False


def MapFrameToTerminal(frame):
    c, l = os.get_terminal_size().columns, os.get_terminal_size().lines
    return cv2.resize(frame, (c, l))


def PixelToAscii(pixel):
    return pixel_set[int((len(pixel_set) - 1) * (1 - numpy.average(pixel) / 255))]


def PixelToAsciiColor(pixel):
    color = f"\033[38;2;{pixel[2]};{pixel[1]};{pixel[0]}m"
    return f"{color}{pixel_set[int((len(pixel_set) - 1) * (1 - numpy.average(pixel) / 255))]}"


def MapIntensity(frame):
    global play_color
    if play_color:
        return ''.join([''.join([PixelToAsciiColor(p) for p in pixel]) for pixel in frame])
    return ''.join([''.join([PixelToAscii(p) for p in pixel]) for pixel in frame])


def PreviewFramerate(file):
    if parameters.fps != 0:
        ManualFPS = parameters.fps
        return ManualFPS
    else:
        video = cv2.VideoCapture(file)
        SourceFPS = video.get(cv2.CAP_PROP_FPS)
        return SourceFPS
    video.release()


def PlayVideoFrames(file):
    video = cv2.VideoCapture(file)
    FrameSleep = ((1 / PreviewFramerate(file)) * 0.564)
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            frame = MapFrameToTerminal(frame)
            frame = MapIntensity(frame)
            print("".join(frame))
            time.sleep(FrameSleep)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


atexit.register(lambda: print("\033[0m"))

parser = ArgumentParser()
parameters = parser.parameters

if os.name == 'nt' and 'color' in parameters:
    print("Color mode probably not supported on Windows, consider switching to better OS")
if 'color' in parameters:
    play_color = parameters.color
if parameters.fps == 0:
    print("Using source framerate")
elif parameters.fps < 0:
    print("-F [--fps] positional argument must be positive")
    exit()

file = parser.GetFile()
PlayVideoFrames(file)
