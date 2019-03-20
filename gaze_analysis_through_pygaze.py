
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

    #(in seconds)
    #start time of video segment you want to extract
    #end time of video segment you want to extract
    #total time of video
    #saveLocation: location where output heatmap is to be saved
    #gazeFilePath: location of gaze csv
    #videoLocation: location of video
    #imageWidth and IimageHeight: dimension of a frame in a video


    saveLocation = '/Users/jeffhe/Desktop/commitments/urap/resources/heatmap_processing/0308_1630_text_02/heatmap.png'
    gazeFilePath = "/Users/jeffhe/Desktop/commitments/urap/resources/heatmap_processing/0308_1630_text_02/gaze_positions.csv"
    videoLocation = "/Users/jeffhe/Desktop/commitments/urap/resources/heatmap_processing/0308_1630_text_02/world.mp4"
    imageWidth = 1280
    imageHeight = 720

    def StartTimeSeconds():
        with open(gazeFilePath) as f:
            reader = csv.reader(f)
            reader = list(reader)
            startTimeSeconds = float(reader[1][0])
        return startTimeSeconds

    startTimeSeconds = StartTimeSeconds() + startTime
    endTimeSeconds = StartTimeSeconds() + endTime

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

    with open(gazeFilePath) as f:
        reader = csv.reader(f)
        line_num = 0
        norm_pos_x = []
        norm_pos_y = []
        timeStamps = []
        for row in reader:
            if (line_num != 0):
                if not (float(row[2]) < 0.5 or float(row[3]) > 1 or float(row[3]) < 0 or float(row[4]) > 1 or float(row[4]) < 0):
                    if (float(row[0]) > startTimeSeconds and float(row[0]) < endTimeSeconds):
                        norm_pos_x += [int(float(row[3]) * 1280)]
                        norm_pos_y += [imageHeight - int(float(row[4]) * 720)]
                        timeStamps += [float(row[0])]
            line_num += 1

    count = 0
    while (count < len(timeStamps)):
        timeStamps[count] *= 1000
        count += 1

    Sfix, Efix = fixation_detection(norm_pos_x,norm_pos_y,timeStamps)


    draw_heatmap(Efix,(imageWidth,imageHeight),image,savefilename=saveLocation)
    #the above function call isn't necessary in Shaantam's case. The fixation data is stored in Efix
    #in the form of [[start time, end time, duration, x-coordinates, y-coordinates][][]...]
    #here, the y-coordinate is calculated from top (meaning that top pixel is 0, bottom pixel is 720)

    return Efix



heatMap(48,52,67)
#call this function to get the Efix fixation data, first parameter is the second of video you want to start analyzing,
#second parameter is where yoou want to stop analyzing
#third one is total time of video