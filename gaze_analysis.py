

# native
import os
import csv
import cv2

# custom
from pygazeanalyser.edfreader import read_edf
from pygazeanalyser.detectors import fixation_detection
from pygazeanalyser.gazeplotter import draw_fixations, draw_heatmap, draw_scanpath, draw_raw

# external
import numpy


def heatMap(startTime,endTime,totalTime):

    #(in seconds) (later converted to millis)
    #start time of video segment
    #end time of video segment
    #total time of video
    #saveLocation: location where output heatmap is to be saved
    #fixationFilePath: location of fixation csv
    #videoLocation: location of video
    #imageWidth and IimageHeight: dimension of a frame in a video



    saveLocation = '/Users/jeffhe/Desktop/commitments/urap/resources/heatmap_processing/0308_1528_manual_03/heatmat.png'
    fixationFilePath = "/Users/jeffhe/Desktop/commitments/urap/resources/heatmap_processing/0308_1528_manual_03/fixations.csv"
    gazeFilePath = "/Users/jeffhe/Desktop/commitments/urap/resources/heatmap_processing/0308_1528_manual_03/gaze_positions.csv"
    videoLocation = "/Users/jeffhe/Desktop/commitments/urap/resources/heatmap_processing/0308_1528_manual_03/worldwithoutgaze.mp4"
    imageWidth = 1280
    imageHeight = 720

    def changeStartTimeMillis():
        with open(gazeFilePath) as f:
            reader = csv.reader(f)
            reader = list(reader)
            startTimeSeconds = float(reader[1][0])
        return startTimeSeconds

    startTimeMillis = changeStartTimeMillis() * 1000



    vidcap = cv2.VideoCapture(videoLocation)
    frames = []
    success, image = vidcap.read()
    frames += [image]
    while success:
        success, image = vidcap.read()
        frames += [image]

    startFrame = (startTime / totalTime) * len(frames)
    endFrame = (endTime / totalTime) * len(frames)
    image = frames[int((startFrame + endFrame) / 2)]


    startTime = startTime * 1000
    endTime = endTime * 1000


    with open(fixationFilePath) as f:
        reader = csv.reader(f)
        line_num = 0
        Efix = []
        for row in reader:
            if (line_num != 0):
                start = float(row[1]) * 1000 - startTimeMillis
                Efix += [[start,start + float(row[2]),float(row[2]),int(float(row[5]) * imageWidth),imageHeight - int(float(row[6]) * imageHeight)]]
            line_num += 1

    i = 0
    while (i < len(Efix)):
        start = Efix[i][0]
        end = Efix[i][1]
        print(startTime,end)
        if (startTime > end):
            Efix.remove(Efix[i])
            continue
        if (endTime < start):
            Efix.remove(Efix[i])
            continue
        i += 1

    draw_heatmap(Efix,(imageWidth,imageHeight),image,savefilename=saveLocation)
    print(Efix)


heatMap(44,53,65)