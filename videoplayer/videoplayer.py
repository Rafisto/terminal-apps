import os
import pytube
import cv2
import atexit
import time
import numpy
from parameters import ArgumentParser
from videoprocessor import VideoProcessor

def DownloadFromYoutube():
    VideoLink = parser.GetYoutube()
    if VideoLink is None:
        print("No video link provided")
        exit()
    else:
        try:
            video = pytube.YouTube(VideoLink)
            video_streams = video.streams.filter(type="video")
            video_streams[1].download("./video", filename="cache.mp4")
        except:
            print("Invalid video link")
            exit()


def PlayVideoFrames(file):
    video = cv2.VideoCapture(file)
    #FrameSleep = ((1 / vp.PreviewFramerate(file)) * 0.564)
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            frame = vp.MapFrameToTerminal(frame)
            frame = vp.MapIntensity(frame)
            print("".join(frame))
            #time.sleep(FrameSleep)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


def RenderVideoFrames():
    video = cv2.VideoCapture(file)
    pre_render = []
    i = 0
    l = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    while video.isOpened():
        i += 1
        ret, frame = video.read()
        if ret:
            print(f"Processing {numpy.round((i / l) * 100, 2)}%", end="\r")
            frame = vp.MapFrameToTerminal(frame)
            frame = vp.MapIntensity(frame)
            pre_render.append("".join(frame))
        else:
            break
    video.release()
    cv2.destroyAllWindows()

    fps = vp.PreviewFramerate(file)
    PlayPreRenderedFrames(pre_render, fps)


def PlayPreRenderedFrames(frames, fps):
    FrameSleep = ((1 / fps) * 0.564)
    for frame in frames:
        print(frame)
        time.sleep(FrameSleep)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    atexit.register(lambda: print("\033[0m"))

    parser = ArgumentParser()
    vp = VideoProcessor(parser)

    file = parser.GetFile()

    if parser.GetPre():
        RenderVideoFrames()
    elif parser.GetYoutube():
        DownloadFromYoutube()
        PlayVideoFrames("./video/cache.mp4")
        os.system(f"rm -rf ./video/cache.mp4")
    else:
        PlayVideoFrames(file)
