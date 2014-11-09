from Tkinter import *

def medianOfColor(mylist):
    length = len(mylist)
    grayScale = [0 for i in range(length)]
    for x in range(length):
        grayScale[x] = (mylist[x][0] + mylist[x][1] + mylist[x][2])/3
    yx = zip(grayScale,mylist)
    yx.sort()
    sorts = [x for (y,x) in yx]
    if not length % 2:
        return (sorts[length/2] + sorts[length/2-1]) / 2.0
    return sorts[length / 2]

medianOfColor([[255,223,23],[25,223,233],[255,23,233],[255,23,233]])