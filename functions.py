import numpy as np


def getBrightness(frame):
    avg = np.sum(frame)/(frame.shape[0]*frame.shape[1])
    avg=avg/255
    if(avg > 0.6):
        return ("OUTDOOR BRIGHT", avg)
    if(avg > 0.4):
        return ("BRIGHT", avg)
    if(avg>0.2):
        return ("Dim", avg)
    else:
        return ("Dark",avg)
