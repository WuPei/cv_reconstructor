from Tkinter import *
import numpy as np
def medianOfColor(mylist):
    length = len(mylist)
    grayScale = [0 for i in range(length)]
    for x in range(length):
        grayScale[x] = int((mylist[x][0] + mylist[x][1] + mylist[x][2])/3)
    sorts = [x for (y,x) in sorted(zip(grayScale,mylist),key = lambda pair:pair[0])]
    if not length % 2:
        return (sorts[length/2] + sorts[length/2-1]) / 2.0
    return sorts[length / 2]

print medianOfColor([np.array([255,223,23]),np.array([25,223,233]),np.array([255,23,233]),np.array([255,23,233])])
