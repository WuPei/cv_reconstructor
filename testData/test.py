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

list_a = [2,55,150,24,434]
list_b = [2,23,214,545,24]
sorts = [(x,y) for (y,x) in sorted(zip(list_a,list_b))]
print sorts