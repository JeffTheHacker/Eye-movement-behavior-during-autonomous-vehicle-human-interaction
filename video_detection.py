#from object_detection_applied_using_KITTY import processImages
from object_detection_applied_using_resnet import processImages
from video_to_frames import convert
import pickle
import cv2

imgArr = []
dictArr = []
finalTable = []
#convert("/Users/jeffhe/Desktop/commitments/urap/week 1/world.mp4","/Users/jeffhe/Desktop/commitments/urap/week 1/frames/")
imgArr, dictArr = processImages("/Users/jeffhe/Desktop/commitments/urap/week 1/frames",357) #miny,minx,maxy,maxx

height,width,channel = imgArr[0].shape

i = 0
while (i < len(dictArr)):
    dictionary = dictArr[i]
    boxes = dictionary['detection_boxes']
    classes = dictionary['detection_classes']
    scores = dictionary['detection_scores']
    j = 0
    print(boxes)
    print(classes)
    while (j < len(boxes)):
        if (not (boxes[j][0] == 0 and boxes[j][1] == 0 and boxes[j][2] == 0 and boxes[j][3] == 0)) and classes[j] == 3: #change this based on the label map
            miny = int(boxes[j][0] * height)
            minx = int(boxes[j][1] * width)
            maxy = int(boxes[j][2] * height)
            maxx = int(boxes[j][3] * width)
            row = [i,miny,minx,maxy,maxx,scores[j]]
            finalTable.append(row)
        j += 1
    i += 1

print(finalTable)
pickle.dump(finalTable,open("finalTable.pickle",'wb'))

count = 0
for i in imgArr:
    cv2.imwrite('/Users/jeffhe/Desktop/commitments/urap/Eye-movement-behavior-during-autonomous-vehicle-human-interaction/video_detection_output' + str(count) + '.png',cv2.cvtColor(i, cv2.COLOR_RGB2BGR))
    count += 1

