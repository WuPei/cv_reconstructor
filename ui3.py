import shape as sp
from Tkinter import *
from PIL import Image, ImageTk


class App:
	def __init__(self, master):
		self.master = master
		self.master.title("cv_recontruction")

		#init parameters
		self.shapes = []
		self.state = 1
		self.currentIndex = -1
		self.newShapeFlag = True
		self.updateRightFrame2Flag = True

		#create object for test purpose
		for i in range(16):
			self.shapes.append(sp.Cylinder([1,2,3],2,3, "cylinder 1"))
			face1 = sp.Face([[20,30]], "Left")
			face2 = sp.Face([[100,100]], "right")
			self.shapes[i*2].faces.append(face1)
			self.shapes[i*2].faces.append(face2)
			self.shapes.append(sp.Cuboid([1,2,3],2,3,4,"cuboid 1"))
		
		self.initUI()
		self.clear()
		
	def initUI(self):
		self.initTopFrames()
		self.initLeftFrame()
		self.initRightFrames()

		#show topframe 1 and right frame
		self.show(self.state)

	def clear(self):
		self.pointId = ""
		self.points =[]
		self.lineIds = []

	def testPrint(self):
		print ""
		print ""
		for x in xrange(len(self.shapes)):
			print self.shapes[x].name
			if isinstance(self.shapes[x], sp.Cylinder):
				print "center = ", self.shapes[x].center 
				print "radius = ", self.shapes[x].radius
				print "height = ", self.shapes[x].height
			elif isinstance(self.shapes[x], sp.Cuboid) or isinstance(self.shapes[self.currentIndex], sp.Prism):
				print "center = ", self.shapes[x].center 
				print "length = ", self.shapes[x].length
				print "width = " , self.shapes[x].width 
				print "height = ", self.shapes[x].height
			elif isinstance(self.shapes[x], sp.Frustum):
				print "center = ", self.shapes[x].center
				print "upperLength = " , self.shapes[x].upperLength
				print "lowerLength = ", self.shapes[x].lowerLength 
				print "upperWidth = " , self.shapes[x].upperWidth 
				print "lowerWidth = " , self.shapes[x].lowerWidth 
				print "height = " , self.shapes[x].height 
			elif isinstance(self.shapes[x], sp.Tree):
				print "center = " , self.shapes[x].center 
				print "height = " , self.shapes[x].height
		print ""

	def fecthRightFrame2Data(self):
		if isinstance(self.shapes[self.currentIndex], sp.Cylinder):
			for i in range(6):
				self.pEntries[i].delete(0, END)

			self.pEntries[1].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[2].insert(0, self.shapes[self.currentIndex].center[1])
			self.pEntries[3].insert(0, self.shapes[self.currentIndex].center[2])
			self.pEntries[4].insert(0, self.shapes[self.currentIndex].radius)
			self.pEntries[5].insert(0, self.shapes[self.currentIndex].height)
		elif isinstance(self.shapes[self.currentIndex], sp.Cuboid) or isinstance(self.shapes[self.currentIndex], sp.Prism):
			for i in range(7):
				self.pEntries[i].delete(0, END)

			self.pEntries[1].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[2].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[3].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[4].insert(0, self.shapes[self.currentIndex].length)
			self.pEntries[5].insert(0, self.shapes[self.currentIndex].width)
			self.pEntries[6].insert(0, self.shapes[self.currentIndex].height)
		elif isinstance(self.shapes[self.currentIndex], sp.Frustum):
			for i in range(9):
				self.pEntries[i].delete(0, END)

			self.pEntries[1].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[2].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[3].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[4].insert(0, self.shapes[self.currentIndex].upperLength)
			self.pEntries[5].insert(0, self.shapes[self.currentIndex].upperWidth)
			self.pEntries[6].insert(0, self.shapes[self.currentIndex].lowerLength)
			self.pEntries[7].insert(0, self.shapes[self.currentIndex].lowerWidth)
			self.pEntries[8].insert(0, self.shapes[self.currentIndex].height)
		elif isinstance(self.shapes[self.currentIndex], sp.Tree):
			for i in range(5):
				self.pEntries[i].delete(0, END)

			self.pEntries[1].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[2].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[3].insert(0, self.shapes[self.currentIndex].center[0])
			self.pEntries[4].insert(0, self.shapes[self.currentIndex].height)

		self.pEntries[0].insert(0,self.shapes[self.currentIndex].name)

	def updateFacesList(self):
		print ""
		print ""
		self.facesList.delete(0,END)
		for item in self.shapes[self.currentIndex].faces:
			print item.faceOrientation
			self.facesList.insert(END, item.faceOrientation) #orientation
		
	#pragma mark -- init frames
	def initTopFrames(self):
		#top frame 1
		self.topFrame1 = Frame(self.master,width =900+20, height = 30, bd=1, relief=SUNKEN)

		self.shape = StringVar(self.master)
		self.shape.set("cylinder") # default value
		self.shapeOptionMenu = OptionMenu(self.topFrame1, self.shape, "cylinder","cuboid","prism","frustum","tree","earth","sky")
		
		self.newShapeButton = Button(self.topFrame1, text = "create new shape",command = self.newShapeButton)

		#top frame 2
		self.topFrame2 = Frame(self.master,width =900+20, height = 30, bd=1, relief=SUNKEN)
		self.cancelButton2 = Button(self.topFrame2, text = "cancel",command = self.cancelButton2)
		self.doneButton2 = Button(self.topFrame2, text = "done", command = self.doneButton2)

		#top frame 3
		self.topFrame3 = Frame(self.master,width =900+20, height = 30, bd=1, relief=SUNKEN)

		self.cancelButton3 = Button(self.topFrame3, text = "cancel",command = self.cancelButton3)
		self.doneButton3 = Button(self.topFrame3, text = "done",command = self.doneButton3)

	def initLeftFrame(self):
		#load image use PIL library
		self.img = Image.open("project.jpeg")
		angle = 180
		tkImage = ImageTk.PhotoImage(self.img.rotate(180))

		#window frame configuration
		self.leftFrame = Frame(self.master)
		self.leftFrame.grid(row = 1,column = 0)
		
		#self.leftFrame.grid_rowconfigure(0, weight=1) #strenth to row
		#self.leftFrame.grid_columnconfigure(0, weight=1)

		#define scroll bar
		xscrollbar = Scrollbar(self.leftFrame, orient=HORIZONTAL)
		xscrollbar.grid(row=1, column=0, sticky=E+W)
		
		yscrollbar = Scrollbar(self.leftFrame)
		yscrollbar.grid(row=0, column=1, sticky=N+S)
		
		#create canvas to load the image
		self.canvas = Canvas(self.leftFrame, width = 900+20, height = 600+20,xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)
		self.canvas.create_image(10, 10,anchor=NW, image=tkImage)
		self.canvas.image = tkImage      #hold a reference
		self.canvas.bind("<Button-1>", self.canvasClicked)
		#canvas.pack(fill = BOTH, expand = 1)
		self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
		
		#config scroll bar
		self.canvas.config(scrollregion=self.canvas.bbox(ALL))
		xscrollbar.config(command=self.canvas.xview)
		yscrollbar.config(command=self.canvas.yview)
		
	def initRightFrames(self):
		self.rightFrame1 = Frame(self.master,width =250, height =600+20+30, bd=1, relief=SUNKEN)
		self.listLabel = Label(self.rightFrame1, text = "All Shapes")
		self.shapesList = Listbox(self.rightFrame1, height = 30)
		for item in self.shapes:
			self.shapesList.insert(END, item.name)
		self.editButton = Button(self.rightFrame1, text = "edit",command = self.editButton1)
		self.deleteButton = Button(self.rightFrame1, text = "delete", command = self.deleteButton)

		#init right frame 2
		self.rightFrame2 = Frame(self.master,width =250, height =600+20+30, bd=1, relief=SUNKEN)
		self.pLabels = [0,0,0,0,0,0,0]
		self.pEntries = [0,0,0,0,0,0,0,0,0]
		for i in xrange(7):
			self.pLabels[i] = Label(self.rightFrame2)
			self.pEntries[i] = Entry(self.rightFrame2)
		for i in range(6,9):
			self.pEntries[i] = Entry(self.rightFrame2)

		self.pEntries[1].config(width = 7)
		self.pEntries[2].config(width = 7)
		self.pEntries[3].config(width = 7)

		self.faceListLabel = Label(self.rightFrame2, text = "All Faces")
		self.facesList = Listbox(self.rightFrame2, height = 15)
		self.addFaceButton = Button(self.rightFrame2, text = "add new face",command = self.addFaceButton)
		self.deleteFaceButton = Button(self.rightFrame2, text = "delete", command = self.deleteFaceButton)


		#init right frame 3
		self.rightFrame3 = Frame(self.master,width =250, height =600+20+30, bd=1, relief=SUNKEN)
		self.faceDirLabel = Label(self.rightFrame3, text="Orientation: ")
		self.faceDir = StringVar(self.master)
		self.faceDir.set("Left") # default value
		self.faceOptionMenu = OptionMenu(self.rightFrame3, self.faceDir, "Left","Right","Upper","Front")

	#pragma mark -- show frames
	def show(self,state):
		if state  == 1:
			self.showTopFrame(1)
			self.showRightFrame(1)
			self.testPrint()
		elif state == 2:
			self.showTopFrame(2)
			self.showRightFrame(2)
		elif state == 3:
			self.showTopFrame(3)
			self.showRightFrame(3)

	def showTopFrame(self,frame):
		if frame == 1:
			self.showTopFrame1(1)
			self.showTopFrame2(0)
			self.showTopFrame3(0)
		elif frame == 2:
			self.showTopFrame1(0)
			self.showTopFrame2(1)
			self.showTopFrame3(0)
		elif frame == 3:
			self.showTopFrame1(0)
			self.showTopFrame2(0)
			self.showTopFrame3(1)

	def showTopFrame1(self,flag):
		if flag == 1:
			self.topFrame1.grid(row = 0,column = 0, sticky=N+S+W+E)
			self.shapeOptionMenu.pack(side = LEFT)
			self.newShapeButton.pack(side = LEFT)
		else:
			self.topFrame1.grid_forget()
			self.shapeOptionMenu.pack_forget()
			self.newShapeButton.pack_forget()

	def showTopFrame2(self,flag):
		if flag == 1:
			self.topFrame2.grid(row = 0, column = 0, sticky=N+S+W+E)
			self.cancelButton2.pack(side = LEFT)
			self.doneButton2.pack(side = RIGHT)
		else:
			self.topFrame2.grid_forget()
			self.cancelButton3.pack_forget()
			self.doneButton3.pack_forget()

	def showTopFrame3(self,flag):
		if flag == 1:
			self.topFrame3.grid(row = 0, column = 0, sticky=N+S+W+E)
			self.cancelButton3.pack(side = LEFT)
			self.doneButton3.pack(side = RIGHT)
		else:
			self.topFrame3.grid_forget()
			self.cancelButton3.pack_forget()
			self.doneButton3.pack_forget()

	def showRightFrame(self,frame):
		if frame == 1:
			self.showRightFrame1(1)
			self.showRightFrame2(0)
			self.showRightFrame3(0)
		elif frame == 2:
			self.showRightFrame1(0)
			self.showRightFrame2(1)
			self.showRightFrame3(0)
		else:
			self.showRightFrame1(0)
			self.showRightFrame2(0)
			self.showRightFrame3(1)

	def showRightFrame1(self,flag):
		if flag == 1:
			self.rightFrame1.grid(column=1, row =0, rowspan = 2, sticky=N+W+E+S)
			self.rightFrame1.pack_propagate(0)
			self.listLabel.pack(fill = X)
			self.shapesList.pack(fill= BOTH)
			self.editButton.pack(fill = X)
			self.deleteButton.pack(fill = X)
		else:
			self.rightFrame1.grid_forget()
			self.listLabel.pack_forget()
			self.shapesList.pack_forget()
			self.editButton.pack_forget()
			self.deleteButton.pack_forget()

	def showRightFrame2(self,flag):
		if flag == 1:
			self.updateFacesList()

			maxRow = 3
			self.rightFrame2.grid(column=1, row =0,  rowspan = 2, sticky=N+W+E+S)
			self.rightFrame2.grid_propagate(0)

			self.pLabels[0].config(text = "name")
			self.pLabels[0].grid(row = 0, column = 0)
			self.pEntries[0].grid(row = 0, column = 1, columnspan = 2)
			if isinstance(self.shapes[self.currentIndex], sp.Cylinder):
				self.pLabels[1].config(text = "center")
				self.pLabels[2].config(text = "radius")
				self.pLabels[3].config(text = "height")

				self.pLabels[1].grid(row = 1, column = 0)
				self.pEntries[1].grid (row = 2, column =0)
				self.pEntries[2].grid (row = 2, column =1)
				self.pEntries[3].grid (row = 2, column =2)
				for i in range(2,4):
					self.pLabels[i].grid(row = i+1, column=0)
					self.pEntries[i+2].grid(row = i+1, column = 1, columnspan = 2)

				maxRow = 4
			elif isinstance(self.shapes[self.currentIndex], sp.Cuboid) or isinstance(self.shapes[self.currentIndex], sp.Prism):
				self.pLabels[1].config(text = "center")
				self.pLabels[2].config(text = "length")
				self.pLabels[3].config(text = "width")
				self.pLabels[4].config(text = "height")

				self.pLabels[1].grid(row = 1, column = 0)
				self.pEntries[1].grid (row = 2, column =0)
				self.pEntries[2].grid (row = 2, column =1)
				self.pEntries[3].grid (row = 2, column =2)
				for i in range(2,5):
					self.pLabels[i].grid(row = i+1, column=0)
					self.pEntries[i+2].grid(row = i+1, column = 1, columnspan = 2)

				maxRow = 5
			elif isinstance(self.shapes[self.currentIndex], sp.Frustum):
				self.pLabels[1].config(text = "center")
				self.pLabels[2].config(text = "upperLength")
				self.pLabels[3].config(text = "upperWidth")
				self.pLabels[4].config(text = "lowerLength")
				self.pLabels[5].config(text = "lowerWidth")
				self.pLabels[6].config(text = "height")

				self.pLabels[1].grid(row = 1, column = 0)
				self.pEntries[1].grid (row = 2, column =0)
				self.pEntries[2].grid (row = 2, column =1)
				self.pEntries[3].grid (row = 2, column =2)
				for i in range(2,7):
					self.pLabels[i].grid(row = i+3, column=0)
					self.pEntries[i+2].grid(row = i+3, column = 1, columnspan = 2)

				maxRow = 7
			elif isinstance(self.shapes[self.currentIndex], sp.Tree):
				self.pLabels[1].config(text = "center")
				self.pLabels[2].config(text = "height")

				self.pLabels[1].grid(row = 1, column = 0)
				self.pEntries[1].grid (row = 2, column =0)
				self.pEntries[2].grid (row = 2, column =1)
				self.pEntries[3].grid (row = 2, column =2)
				
				self.pLabels[2].grid(row = 3, column=0)
				self.pEntries[4+2].grid(row = 3, column = 1 , columnspan = 2)

				maxRow = 3

			self.faceListLabel.grid(row = maxRow+2, column = 0, columnspan = 3)
			self.facesList.grid(row = maxRow+3, column=0, columnspan = 3)
			self.addFaceButton.grid(row = maxRow + 5, column = 0, columnspan = 3)
			self.deleteFaceButton.grid(row = maxRow+6, column = 0, columnspan = 3)

			if self.updateRightFrame2Flag == True:
				self.fecthRightFrame2Data()


		else:
			self.rightFrame2.grid_forget()
			self.doneButton2.grid_forget()
			self.cancelButton2.grid_forget()
			for i in range(7):
				self.pLabels[i].grid_forget()
				self.pEntries[i].grid_forget()
			self.faceListLabel.grid_forget()
			self.facesList.grid_forget()
			self.addFaceButton.grid_forget()
			self.deleteFaceButton.grid_forget()

	def showRightFrame3(self,flag):
		if flag == 1:
			self.rightFrame3.grid(column=1, row =0,  rowspan = 2, sticky=N)
			self.rightFrame3.grid_propagate(0)
			self.faceDirLabel.grid(row = 0, column = 0, sticky = S+N+W+E)
			self.faceOptionMenu.grid(row = 1, column = 0, sticky = S+N+W+E)
		else:
			self.rightFrame3.grid_forget()
			self.faceDirLabel.grid_forget()
			self.faceOptionMenu.grid_forget()	

	#pragma mark -- button actions
	#buttons in scene 1
	def newShapeButton(self):
		self.newShapeFlag = True
		self.updateRightFrame2Flag = True;
		self.currentIndex = len(self.shapes)
		if self.shape.get() == "cylinder":
			self.shapes.append( sp.Cylinder([0,0,0],0,0,""))

		elif self.shape.get() == "cuboid":
			self.shapes.append( sp.Cuboid([0,0,0],0,0,0,"") )

		elif self.shape.get() == "prism":
			self.shapes.append( sp.Prism([0,0,0],0,0,0,"") )

		elif self.shape.get() == "frustum":
			self.shapes.append( sp.Frustum([0,0,0],0,0,0,0,0,"") )

		elif self.shape.get() == "tree":
			self.shapes.append( sp.Tree([0,0,0],0,"") )

		elif self.shape.get() == "sky":
			self.shapes.append( sp.Sky([],"") )

		elif self.shape.get() == "ground":
			self.shapes.append( sp.Ground([],"") )
		
		self.show(2)
		self.state = 2

	def editButton1(self):
		self.newShapeFlag = False
		self.updateRightFrame2Flag = True
		self.currentIndex = (self.shapesList.curselection())[0]
		self.show(2)
		self.state = 2

	def deleteButton(self):
		index = (self.shapesList.curselection())[0]
		del self.shapes[index]
		self.shapesList.delete(index)

	#buttons in scene 2
	def addFaceButton(self):
		self.updateRightFrame2Flag = False
		self.show(3)
		self.state = 3

	def cancelButton2(self):
		if self.newShapeFlag == True:
			del self.shapes[self.currentIndex]
		self.show(1)
		self.state = 1

	def doneButton2(self):
		#save changes only when name is not empty
		if self.pEntries[0].get()!= "":
			self.shapes[self.currentIndex].name = self.pEntries[0].get()
			if isinstance(self.shapes[self.currentIndex], sp.Cylinder):
				x = self.pEntries[1].get()
				y = self.pEntries[2].get()
				z = self.pEntries[3].get()
				self.shapes[self.currentIndex].center = [x,y,z]
				self.shapes[self.currentIndex].radius = self.pEntries[4].get()
				self.shapes[self.currentIndex].height = self.pEntries[5].get()
			elif isinstance(self.shapes[self.currentIndex], sp.Cuboid) or isinstance(self.shapes[self.currentIndex], sp.Prism):
				x = self.pEntries[1].get()
				y = self.pEntries[2].get()
				z = self.pEntries[3].get()
				self.shapes[self.currentIndex].center = [x,y,z]
				self.shapes[self.currentIndex].length = self.pEntries[4].get()
				self.shapes[self.currentIndex].width  = self.pEntries[5].get()
				self.shapes[self.currentIndex].height = self.pEntries[6].get()
			elif isinstance(self.shapes[self.currentIndex], sp.Frustum):
				x = self.pEntries[1].get()
				y = self.pEntries[2].get()
				z = self.pEntries[3].get()
				self.shapes[self.currentIndex].center = [x,y,z]
				self.shapes[self.currentIndex].upperLength = self.pEntries[4].get()
				self.shapes[self.currentIndex].upperWidth  = self.pEntries[5].get()
				self.shapes[self.currentIndex].lowerLength = self.pEntries[6].get()
				self.shapes[self.currentIndex].lowerWidth  = self.pEntries[7].get()
				self.shapes[self.currentIndex].height      = self.pEntries[8].get()
			elif isinstance(self.shapes[self.currentIndex], sp.Tree):
				x = self.pEntries[1].get()
				y = self.pEntries[2].get()
				z = self.pEntries[3].get()
				self.shapes[self.currentIndex].center = [x,y,z]
				self.shapes[self.currentIndex].height = self.pEntries[4].get()

			if self.newShapeFlag == True:
				self.shapesList.insert(END, self.shapes[self.currentIndex].name)
			else:
				self.shapesList.delete(self.currentIndex)
				self.shapesList.insert(self.currentIndex, self.shapes[self.currentIndex].name)
				

			self.show(1)
			self.state = 1

	def deleteFaceButton(self):
		index = (self.facesList.curselection())[0]
		if (index < len(self.shapes[self.currentIndex].faces)):
			for i in range(len(self.shapes[self.currentIndex].faces[index].lineIds)):
				self.canvas.delete(self.shapes[self.currentIndex].faces[index].lineIds[i])
			del self.shapes[self.currentIndex].faces[index]
			self.facesList.delete(index)

	#buttons in scene 3
	def cancelButton3(self):
		if isinstance(self.shapes[self.currentIndex], sp.Shape):
			self.canvas.delete(self.pointId)
			for i in range(len(self.lineIds)):
				self.canvas.delete(self.lineIds[i])
		self.clear()
		self.show(2)
		self.state = 2

	def doneButton3(self):
		if isinstance(self.shapes[self.currentIndex], sp.Shape):
			pLen = len(self.points)
			lineId = self.canvas.create_line(self.points[pLen-1][0],self.points[pLen-1][1],self.points[0][0],self.points[0][1] ,fill = "red")
			self.lineIds.append(lineId)
			face = sp.Face(self.points, self.faceDir.get())
			face.lineIds = self.lineIds
			self.shapes[self.currentIndex].faces.append (face)
		self.clear()
		self.show(2)
		self.state = 2


	#pragma mark -- canvas draw
	def drawPoint(self,p):
		return self.canvas.create_oval(p[0],p[1],p[0],p[1] ,fill = "red", outline = "red")

	def canvasClicked(self,event):
		if self.state == 3:
			x = self.canvas.canvasx(event.x)
			y = self.canvas.canvasy(event.y)
			lineId = ""
			self.points.append([x,y])
			pLen = len(self.points)
			if (pLen == 1):
				self.pointId = self.drawPoint([x,y])
			elif (pLen==2):
				self.canvas.delete(self.pointId)
				lineId = self.canvas.create_line(self.points[pLen-2][0],self.points[pLen-2][1],x,y ,fill = "red")
				self.lineIds.append(lineId)
			else:
				lineId = self.canvas.create_line(self.points[pLen-2][0],self.points[pLen-2][1],x,y ,fill = "red")
				self.lineIds.append(lineId)



root = Tk()
root.resizable(width=FALSE, height=FALSE)
app = App(root)
root.mainloop()
		





