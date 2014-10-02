from Tkinter import *
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        master.title("cv_recontruction")
        
        self.initUI(master)
        self.rectangle = Rectangle([],[],self.canvas)
        self.polygon = Polygon([],self.canvas)
        self.lineIds = []
        self.clear()
    
    def initUI(self,master):
        #load image use PIL library
        self.img = Image.open("project.jpeg")
        angle = 180
        tkImage = ImageTk.PhotoImage(self.img.rotate(180))
        
        #top bar frame
        topFrame = Frame(master,width =self.img.size[0]+20,height = 30)
        topFrame.grid(row = 0, column =0)
        topFrame.pack()
        topFrame.pack_propagate(0)

        self.rectangleButton = Button(topFrame,text="rectangle",command = self.rectangleButton)
        self.polygonButton = Button(topFrame,text="polygon",command = self.polygonButton)

        self.doneButton = Button(topFrame,text = "done",command = self.doneButton)
        self.cancelButton = Button(topFrame,text = "cancel",command = self.cancelButton)
        self.showTopButtons()
        

        #frame of canvas + scroll bar
        frame = Frame(master)
        frame.grid(row = 1,column = 0)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        #define scroll bar
        xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E+W)
        
        yscrollbar = Scrollbar(frame)
        yscrollbar.grid(row=0, column=1, sticky=N+S)

        #create canvas to load the image
        self.canvas = Canvas(frame, width = self.img.size[0]+20 , height = self.img.size[1]+20,xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)
        self.canvas.create_image(10, 10,anchor=NW, image=tkImage)
        self.canvas.image = tkImage      #hold a reference
        self.canvas.bind("<Button-1>", self.canvasClicked)
        #canvas.pack(fill = BOTH, expand = 1)
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)

        
        #config scroll bar
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        xscrollbar.config(command=self.canvas.xview)
        yscrollbar.config(command=self.canvas.yview)

        frame.pack()
    
    def hideTopButtons(self):
        self.rectangleButton.pack_forget()
        self.polygonButton.pack_forget()
    def showTopButtons(self):
        self.rectangleButton.pack(side=LEFT)
        self.polygonButton.pack(side = LEFT)
    def clear(self):
        self.rec_flag = 0
        self.polygon_flag = 0
        self.count_points = 0
        self.rectangle.clear()
        self.polygon.clear()
    
    def drawPoint(self,p):
        return self.canvas.create_oval(p[0],p[1],p[0],p[1])

    def rectangleButton(self):
        self.hideTopButtons()
        self.doneButton.pack(side = RIGHT)
        self.cancelButton.pack(side = LEFT)
        self.rec_flag = 1
    
    def polygonButton(self):
        self.hideTopButtons()
        self.doneButton.pack(side = RIGHT)
        self.cancelButton.pack(side = LEFT)
        self.polygon_flag = 1
        self.polygon_count =0
    
    def doneButton(self):
        self.showTopButtons()
        self.doneButton.pack_forget()
        self.cancelButton.pack_forget()
        if self.polygon_flag == 1:
            self.polygon.draw()
            for i in self.lineIds:
                self.canvas.delete(i)

        #to do: save data
        self.clear()
    
    def cancelButton(self):
        self.showTopButtons()
        self.doneButton.pack_forget()
        self.cancelButton.pack_forget()
        #erase what have been drawn
        if(self.rec_flag == 1):
            self.rectangle.delete()
        elif (self.polygon_flag == 1):
            for i in self.lineIds:
                self.canvas.delete(i)
    
        self.clear()
    
    def canvasClicked(self,event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if (self.rec_flag == 1):
            if (self.rectangle.p1 == []):
                self.rectangle.p1 = [x, y]
                self.pointId = self.drawPoint(self.rectangle.p1)
            else:
                if (self.rectangle.p2 == []):
                    self.rectangle.p2 = [x, y]
                    self.canvas.delete(self.pointId)
                    self.rectangle.draw()
        elif(self.polygon_flag == 1):
            #save the point
            self.polygon.points.append([x,y])
            
            #draw polygon lines
            pLen = len(self.polygon.points)
            if pLen >2 :
                lineId = self.canvas.create_line(self.polygon.points[pLen-2][0],self.polygon.points[pLen-2][1],x,y)
                self.lineIds.append(lineId)
            elif pLen == 1:
                self.pointId = self.drawPoint([x,y])
            elif pLen ==2:
                self.canvas.delete(self.pointId)
                lineId = self.canvas.create_line(self.polygon.points[pLen-2][0],self.polygon.points[pLen-2][1],x,y)
                self.lineIds.append (lineId)









class Rectangle:
    def __init__(self,p1,p2,canvas):
        self.p1 = p1
        self.p2 = p2
        self.canvas = canvas
    def clear(self):
        self.p1 = []
        self.p2 = []
    def draw(self):
        self.recId = self.canvas.create_rectangle(self.p1[0],self.p1[1],self.p2[0],self.p2[1])
    def delete(self):
        self.canvas.delete(self.recId)
    def propertyUI(self):
        #to do : to pop out a window to let users to type in properties
        print "propertyUI"

class Polygon:
    def __init__(self,points,canvas):
        self.points = points
        self.canvas = canvas
    def clear(self):
        self.points = []
    def draw(self):
        self.poId = self.canvas.create_polygon(self.points,fill = '',outline = 'black')
    def delete(self):
        self.canvas.delete(self.poId)





root = Tk()
app = App(root)
root.mainloop()
#root.destroy() # optional; see description below