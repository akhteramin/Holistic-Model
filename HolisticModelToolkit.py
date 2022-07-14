import json
import os
occlusionPercentage={}
caption = []
constant = {
    "news": 6.5541,
    "emergency": 6.9791,
    "interviews": 6.8963,
    "weather": 7.14633,
    "political": 6.3792,
    "sports": 6.7887,
}

def calculateOcclusionScore(weights, OC, genre, occlusionPercentage, occlusionTime):
    # print(weights[genre])
    # print(OC[genre])
    totalOcclusionScore= constant.get(genre)
    for key in occlusionPercentage:
        if OC[genre][key]==1:
            totalOcclusionScore = totalOcclusionScore + occlusionPercentage[key]*weights[genre][key]
        else:
            totalOcclusionScore = totalOcclusionScore + occlusionTime[key]*weights[genre][key]

    return totalOcclusionScore


def calculateOcclusionPercentage(captionArea,itemArea):
    xA = max(captionArea[0], itemArea[0])
    yA = max(captionArea[1], itemArea[1])
    xB = min(captionArea[2], itemArea[2])
    yB = min(captionArea[3], itemArea[3])
    # print(xA, yA, xB, yB)
    # compute the area of intersection rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    # print(interArea)
    if interArea == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = abs((captionArea[2] - captionArea[0]) * (captionArea[3] - captionArea[1]))
    boxBArea = abs((itemArea[2] - itemArea[0]) * (itemArea[3] - itemArea[1]))

    # areas - the interesection area
    # iou = interArea / float(boxAArea + boxBArea - interArea)
    iou = interArea / float(boxBArea)

    # return the intersection over union value
    return iou

def initObjects(data):
    global occlusionTime
    occlusionTime = {}
    for frame in data:
        # print(type(frame))
        for key in frame:
            # print(key)
            if key=='Caption':
                caption = frame[key]
            else:
                occlusionArea = calculateOcclusionPercentage(caption,frame[key])

                occlusionPercentage[key] = max(occlusionPercentage.get(key, 0),occlusionArea)
                occlusionTime[key] = occlusionTime.get(key,0)
                if occlusionArea>0:
                    occlusionTime[key] = occlusionTime[key] + 1
    if len(occlusionTime)>0:
        occlusionTime = {k: v / len(occlusionTime) for total in (sum(occlusionTime.values()),) for k, v in occlusionTime.items()}

    # print(occlusionPercentage)
    # print(occlusionTime)

        # occlusionPercentage = {frame[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        # occlusionTime = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}

def generateOcclusionScore():
    file=open("input.json")
    data = json.load(file)
    file.close()
    # -------------------------------
    weightfile = open("weights.json")
    weights = json.load(weightfile)
    weightfile.close()
    # ----------------------------------
    occlusionCriteria = open("occlusioncriteria.json")
    OC = json.load(occlusionCriteria)
    occlusionCriteria.close()
    # ----------------------------------

    initObjects(data['frames'])
    score = calculateOcclusionScore(weights, OC, data['genre'], occlusionPercentage, occlusionTime)
    print("Quality Score: ",1-score)
    result_file = open("result.txt", "w+")
    result_file.write("Quality Score: " + str(1-score) + "\n")
generateOcclusionScore()
