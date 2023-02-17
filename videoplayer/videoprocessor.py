import os
import cv2
import numpy

pixel_set = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"


class VideoProcessor:
    def __init__(self, parser):
        self.parser = parser

    def MapFrameToTerminal(self, frame):
        c, l = os.get_terminal_size().columns, os.get_terminal_size().lines
        return cv2.resize(frame, (c, l))

    def PixelToAscii(self, pixel):
        return pixel_set[int((len(pixel_set) - 1) * (1 - numpy.average(pixel) / 255))]

    def PixelToAsciiColor(self, pixel):
        color = f"\033[38;2;{pixel[2]};{pixel[1]};{pixel[0]}m"
        return f"{color}{pixel_set[int((len(pixel_set) - 1) * (1 - numpy.average(pixel) / 255))]}"

    def MapIntensity(self, frame):
        if self.parser.GetColor():
            return ''.join([''.join([self.PixelToAsciiColor(p) for p in pixel]) for pixel in frame])
        return ''.join([''.join([self.PixelToAscii(p) for p in pixel]) for pixel in frame])

    def PreviewFramerate(self, file):
        if self.parser.GetFPS() != 0:
            ManualFPS = self.parser.GetFPS()
            return ManualFPS
        else:
            video = cv2.VideoCapture(file)
            SourceFPS = video.get(cv2.CAP_PROP_FPS)
            return SourceFPS
