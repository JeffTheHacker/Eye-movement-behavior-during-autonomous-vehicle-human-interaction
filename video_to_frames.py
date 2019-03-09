import cv2

def convert(videoLocation,frameLocation):
    vidcap = cv2.VideoCapture(videoLocation)
    success, image = vidcap.read()
    count = 0
    while success:
        countstr = str(count)
        cv2.imwrite(frameLocation + countstr.zfill(5) + ".jpg", image)
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1