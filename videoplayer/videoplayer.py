import argparse
import os
import cv2
import numpy
import atexit
import time

argument_parser = argparse.ArgumentParser(description="Terminal Video Player",
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
argument_parser.add_argument("-f", "--file", help="Video file to play")
argument_parser.add_argument("-c", "--color", help="Color mode", action='store_true')
argument_parser.add_argument("-p", "--pre", help="Pre-render video", action='store_true')
argument_parser.add_argument("-s", "--save", help="Save pre-rendered video", action='store_true')
argument_parser.add_argument("-F", "--fps", help="Framerate of the video (will use the framerate of the original video if not specified)", type=int, default=0)
argument_parser.usage = "videoplayer.py [-h for help]"

pixel_set = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
play_color = False


def CheckFileExists(file):
    if not os.path.isfile(file):
        raise argparse.ArgumentTypeError("File not found")
    return file


def CheckHelp(parameters):
    if 'help' in parameters:
        argument_parser.print_help()
        exit()


def MapFrameToTerminal(frame):
    c, l = os.get_terminal_size().columns, os.get_terminal_size().lines
    return cv2.resize(frame, (c, l))


def PixelToAscii(pixel):
    return pixel_set[int((len(pixel_set) - 1) * (1 - numpy.average(pixel) / 255))]


def PixelToAsciiColor(pixel):
    return f"\033[38;2;{pixel[2]};{pixel[1]};{pixel[0]}m{pixel_set[int((len(pixel_set) - 1) * (1 - numpy.average(pixel) / 255))]}"


def MapIntensity(frame):
    global play_color
    if play_color:
        return ''.join([''.join([PixelToAsciiColor(p) for p in pixel]) for pixel in frame])
    return ''.join([''.join([PixelToAscii(p) for p in pixel]) for pixel in frame])


def PreviewFramerate(file):
    parameters = argument_parser.parse_args()
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

parameters = argument_parser.parse_args()
CheckHelp(parameters)

if os.name == 'nt' and 'color' in parameters:
    print("Color mode probably not supported on Windows, consider switching to better OS")
if 'color' in parameters:
    play_color = parameters.color

file = CheckFileExists(parameters.file)
PlayVideoFrames(file)

