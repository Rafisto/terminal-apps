import cv2


def PlayVideoFrames(file):
    video = cv2.VideoCapture(file)
    prev_frame = video.read()[0]
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            cv2.imshow("frame", cv2.absdiff(frame, prev_frame))
            prev_frame = frame
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


PlayVideoFrames("../videoplayer/Bad_Apple.mp4")
