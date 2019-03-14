

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
    #start time of video segment
    #end time of video segment
    #total time of video
    #saveLocation: location where output heatmap is to be saved
    #gazeFilePath: location of gaze csv
    #videoLocation: location of video
    #imageWidth and IimageHeight: dimension of a frame in a video


    saveLocation = '/Users/jeffhe/Desktop/commitments/urap/Eye-movement-behavior-during-autonomous-vehicle-human-interaction/heatmap_output/heatmat.png'
    gazeFilePath = "/Users/jeffhe/Desktop/commitments/urap/resources/pupil recordings/2019 02 07 13 40 29 AV Symbols 2/exports/overlayed/gaze_positions.csv"
    videoLocation = "/Users/jeffhe/Desktop/commitments/urap/resources/pupil recordings/2019 02 07 13 40 29 AV Symbols 2/exports/original/world.mp4"
    imageWidth = 1280
    imageHeight = 720

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
        for row in reader:
            if (line_num != 0):
                if not (float(row[2]) < 0.5 or float(row[3]) > 1 or float(row[3]) < 0 or float(row[4]) > 1 or float(row[4]) < 0):
                    norm_pos_x += [int(float(row[3]) * 1280)]
                    norm_pos_y += [imageHeight - int(float(row[4]) * 720)]
            line_num += 1

    startRow = (startTime / totalTime) * line_num
    endRow = (endTime / totalTime) * line_num

    norm_pos_x = norm_pos_x[int(startRow):int(endRow)]
    norm_pos_y = norm_pos_y[int(startRow):int(endRow)]

    Sfix, Efix = fixation_detection(norm_pos_x,norm_pos_y,range(len(norm_pos_x)))


    draw_heatmap(Efix,(imageWidth,imageHeight),image,savefilename=saveLocation)


heatMap(70,142,158)