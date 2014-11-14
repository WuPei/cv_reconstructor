from Tkinter import *
import os
import videoMaker as vmaker

width = 1632
height = 1224

files = []
#add construction process to video
for i in range(26):
    filename = os.path.join("construction","points_"+str(i)+".png")
    for j in range(3):
        files.append(filename)
for i in range(26):
    filename = os.path.join("construction","img_"+str(i)+".png")
    for j in range(3):
        files.append(filename)

#dir = ["path1","path2","path3","path4","path5"]
dir = ["path1","path2","path3","path5"]
#lenOfPath = [112,25,90,13,13]
lenOfPath = [112,25,90,13]
for i in range(len(dir)):
    filesOfEachPath = []
    for x in range(lenOfPath[i]):
        if dir[i]=="path5":
            filename = os.path.join(dir[i],"result_"+str(x+12)+".png")
            if filename == os.path.join(dir[i],"result_24.png"):
                for t in range(24):
                     filesOfEachPath.append(filename)      
        else:
            filename = os.path.join(dir[i],"result_"+str(x)+".png")
        filesOfEachPath.append(filename)
    if dir[i]=="path3":
        files.extend(filesOfEachPath)
        files.extend(filesOfEachPath[::-1])
    elif dir[i]=="path4":
        files.extend(filesOfEachPath[::-1])
        files.extend(filesOfEachPath)
    else:
        files.extend(filesOfEachPath)

for file in files:
    print file+"\n"

vm = vmaker.VideoMaker(len(files), width, height)
vm.generateVideoFromFiles(files)
print "------------Video-Making Part Finished------------"
print "------------Thanks for using cvreconstructor------------"
print "-----Created by:Wu Pei,Wu Dan,Fang Zhou, Zhou bin Nov,2014------------"