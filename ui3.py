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
		self.currentShape = "new"
		self.newShapeFlag = True

		#create object for test purpose
		cylinder = sp.Cylinder(1,1,1, "cylinder 1")
		cylinder.addFace([20,30], "Left")
		cylinder.addFace([10,30], "Right")
		cylinder.addFace([20,30], "Upper")
		cylinder.addFace([20,30], "Front")
		cuboid = sp.Cuboid(1,1,1,1,"cuboid 1")
		for i in range(16):
			self.shapes.append(cylinder)
			self.shapes.append(cuboid)
		
		self.initUI()
		self.clear()
		
	def initUI(self):
		self.initTopFrames()
		self.initLeftFrame()
		self.initRightFrames()

		#show topframe 1 and right frame
		self.show(self.state)

	def clear(self):
		self.flag = ""
		self.pointId = ""
		self.drawId = ""
		self.points =[]
		self.models = []
		self.lineIds = []

	def updateFacesList(self):
		if self.newShapeFlag == False:
			for item in self.currentShape.faces:
				print item[1]
				self.facesList.insert(END, item[1]) #orientation
		
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

		self.face = StringVar(self.master)
		self.face.set("Rectangle") # default value
		self.faceOptionMenu = OptionMenu(self.topFrame2, self.face, "rectangle","circle","polygon")
		
		self.addFaceButton = Button(self.topFrame2, text = "add new face",command = self.addFaceButton)

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
		self.cancelButton2 = Button(self.rightFrame2, text = "cancel",command = self.cancelButton2)
		self.doneButton2 = Button(self.rightFrame2, text = "done", command = self.doneButton2)
		self.pLabels = [0,0,0,0,0,0,0]
		self.pEntries = [0,0,0,0,0,0,0]
		for i in xrange(7):
			self.pLabels[i] = Label(self.rightFrame2)
			self.pEntries[i] = Entry(self.rightFrame2)

		self.faceListLabel = Label(self.rightFrame2, text = "All Faces")
		self.facesList = Listbox(self.rightFrame2, height = 15)
		self.editFaceButton = Button(self.rightFrame2, text = "edit",command = self.editFaceButton)
		self.deleteFaceButton = Button(self.rightFrame2, text = "delete", command = self.deleteFaceButton)

		#init right frame 3
		self.rightFrame3 = Frame(self.master,width =250, height =600+20+30, bd=1, relief=SUNKEN)
		self.faceDirLabel = Label(self.rightFrame3, text="Orientation: ")
		self.faceDirEntry = Entry(self.rightFrame3)

	#pragma mark -- show frames
	def show(self,state):
		if state  == 1:
			self.showTopFrame(1)
			self.showRightFrame(1)
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
			self.faceOptionMenu.pack(side = LEFT)
			self.addFaceButton.pack(side = LEFT)
		else:
			self.topFrame2.grid_forget()
			self.faceOptionMenu.pack_forget()
			self.addFaceButton.pack_forget()

	def showTopFrame3(self,flag):
		if flag == 1:
			self.topFrame3.grid(row = 0, column = 0, sticky=N+S+W+E)
			self.cancelButton3.pack(side = LEFT)
			self.doneButton3.pack(side = LEFT)
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

			maxRow = 2
			self.rightFrame2.grid(column=1, row =0,  rowspan = 2, sticky=N+W+E+S)
			self.rightFrame2.grid_propagate(0)
			self.doneButton2.grid(row = 0, columnspan = 2)
			self.cancelButton2.grid(row =1, columnspan =2)

			self.pLabels[0].config(text = "name")
			self.pLabels[0].grid(row = 2, column = 0)
			if isinstance(self.currentShape, sp.Cylinder):
				self.pLabels[1].config(text = "center")
				self.pLabels[2].config(text = "radius")
				self.pLabels[3].config(text = "height")
				for i in range(4):
					self.pLabels[i].grid(row = i+2, column=0)
					self.pEntries[i].grid(row = i+2, column = 1)
					self.pEntries[i].delete(0, END)

				self.pEntries[1].insert(0, self.currentShape.center)
				self.pEntries[2].insert(0, self.currentShape.radius)
				self.pEntries[3].insert(0, self.currentShape.height)

				maxRow = 5
			elif isinstance(self.currentShape, sp.Cuboid) or isinstance(self.currentShape, sp.Prism):
				self.pLabels[1].config(text = "center")
				self.pLabels[2].config(text = "length")
				self.pLabels[3].config(text = "width")
				self.pLabels[4].config(text = "height")
				for i in range(5):
					self.pLabels[i].grid(row = i+2, column=0)
					self.pEntries[i].grid(row = i+2, column = 1)
					self.pEntries[i].delete(0, END)

				self.pEntries[1].insert(0, self.currentShape.center)
				self.pEntries[2].insert(0, self.currentShape.length)
				self.pEntries[3].insert(0, self.currentShape.width)
				self.pEntries[4].insert(0, self.currentShape.height)

				maxRow = 6
			elif isinstance(self.currentShape, sp.Frustum):
				self.pLabels[1].config(text = "center")
				self.pLabels[2].config(text = "upperLength")
				self.pLabels[3].config(text = "upperWidth")
				self.pLabels[4].config(text = "lowerLength")
				self.pLabels[5].config(text = "lowerWidth")
				self.pLabels[6].config(text = "height")
				for i in range(7):
					self.pLabels[i].grid(row = i+2, column=0)
					self.pEntries[i].grid(row = i+2, column = 1)
					self.pEntries[i].delete(0, END)

				self.pEntries[1].insert(0, self.currentShape.center)
				self.pEntries[2].insert(0, self.currentShape.upperLength)
				self.pEntries[3].insert(0, self.currentShape.upperWidth)
				self.pEntries[4].insert(0, self.currentShape.lowerLength)
				self.pEntries[5].insert(0, self.currentShape.lowerWidth)
				self.pEntries[6].insert(0, self.currentShape.height)

				maxRow = 8
			elif isinstance(self.currentShape, sp.Tree):
				self.pLabels[1].config(text = "center")
				self.pLabels[2].config(text = "height")
				for i in range(3):
					self.pLabels[i].grid(row = i+2, column=0)
					self.pEntries[i].grid(row = i+2, column = 1)
					self.pEntries[i].delete(0, END)

				self.pEntries[1].insert(0, self.currentShape.center)
				self.pEntries[2].insert(0, self.currentShape.height)

				maxRow = 4

			self.pEntries[0].insert(0,self.currentShape.name)

			self.faceListLabel.grid(row = maxRow+2, column = 0, columnspan = 2)
			self.facesList.grid(row = maxRow+3, column=0, columnspan = 2)
			self.editFaceButton.grid(row = maxRow +4, column = 0, columnspan = 2)
			self.deleteFaceButton.grid(row = maxRow+5, column = 0, columnspan = 2)

		else:
			self.rightFrame2.grid_forget()
			self.doneButton2.grid_forget()
			self.cancelButton2.grid_forget()
			for i in range(7):
				self.pLabels[i].grid_forget()
				self.pEntries[i].grid_forget()
			self.faceListLabel.grid_forget()
			self.facesList.grid_forget()
			self.editFaceButton.grid_forget()
			self.deleteFaceButton.grid_forget()

	def showRightFrame3(self,flag):
		if flag == 1:
			self.rightFrame3.grid(column=1, row =0,  rowspan = 2, sticky=N)
			self.rightFrame3.grid_propagate(0)
			self.faceDirLabel.grid(row = 0, column = 0, sticky = W)
			self.faceDirEntry.grid(row = 1, column = 0, sticky = W)
		else:
			self.rightFrame3.grid_forget()
			self.faceDirLabel.grid_forget()
			self.faceDirEntry.grid_forget()	

	#pragma mark -- button actions
	#buttons in scene 1
	def newShapeButton(self):
		self.newShapeFlag = True
		if self.shape.get() == "cylinder":
			self.currentShape = sp.Cylinder(0,0,0,"")

		elif self.shape.get() == "cuboid":
			self.currentShape = sp.Cuboid(0,0,0,0,"")

		elif self.shape.get() == "prism":
			self.currentShape = sp.Prism(0,0,0,0,"")

		elif self.shape.get() == "frustum":
			self.currentShape = sp.Frustum(0,0,0,0,0,0,"")

		elif self.shape.get() == "tree":
			self.currentShape = sp.Tree(0,0,"")

		elif self.shape.get() == "sky":
			self.currentShape = sp.Sky([],"")

		elif self.shape.get() == "ground":
			self.currentShape = sp.Ground([],"")
		
		self.show(2)
		self.state = 2

	def editButton1(self):
		self.newShapeFlag = False
		index = (self.shapesList.curselection())[0]
		self.currentShape = self.shapes[index]
		self.show(2)
		self.state = 2

	def deleteButton(self):
		index = (self.shapesList.curselection())[0]
		del self.shapes[index]
		self.shapesList.delete(index)

	#buttons in scene 2
	def addFaceButton(self):
		self.show(3)
		self.state = 3

	def cancelButton2(self):
		self.show(1)
		self.state = 1

	def doneButton2(self):
		#save changes
		self.currentShape.name = self.pEntries[0].get()
		if isinstance(self.currentShape, sp.Cylinder):
			self.currentShape.center = self.pEntries[1].get()
			self.currentShape.radius = self.pEntries[2].get()
			self.currentShape.height = self.pEntries[3].get()
		elif isinstance(self.currentShape, sp.Cuboid) or isinstance(self.currentShape, sp.Prism):
			self.currentShape.center = self.pEntries[1].get()
			self.currentShape.length = self.pEntries[2].get()
			self.currentShape.width  = self.pEntries[3].get()
			self.currentShape.height = self.pEntries[4].get()
		elif isinstance(self.currentShape, sp.Frustum):
			self.currentShape.center = self.pEntries[1].get()
			self.currentShape.upperLength = self.pEntries[2].get()
			self.currentShape.upperWidth  = self.pEntries[3].get()
			self.currentShape.lowerLength = self.pEntries[4].get()
			self.currentShape.lowerWidth = self.pEntries[5].get()
			self.currentShape.height = self.pEntries[6].get()
		elif isinstance(self.currentShape, sp.Tree):
			self.currentShape.center = self.pEntries[1].get()
			self.currentShape.height = self.pEntries[2].get()

		if self.newShapeFlag == True:
			self.shapesList.insert(END, self.currentShape.name)
			self.shapes.append(self.currentShape)
		else:
			index = (self.shapesList.curselection())[0]
			#update array and listBox
			del self.shapes[index]
			self.shapes.insert(index, self.currentShape)
			self.shapesList.delete(index)
			self.shapesList.insert(index, self.currentShape.name)

		self.show(1)
		self.state = 1

	def editFaceButton(self):
		print "2"
	def deleteFaceButton(self):
		print "2"

	#buttons in scene 3
	def cancelButton3(self):
		self.show(2)
		self.state = 2

	def doneButton3(self):
		self.show(2)
		self.state = 2


	#pragma mark -- click event	
	def canvasClicked(self,event):
		if self.state == 3:
			x = self.canvas.canvasx(event.x)
			y = self.canvas.canvasy(event.y)
			if (self.flag == "drawRect"):
				if ( len(self.points) == 0):
					self.points.append ([x, y])
					self.pointId = self.drawPoint([x,y])
				elif( len(self.points) == 1):
						self.points.append ([x, y])
						self.canvas.delete(self.pointId)
						self.drawId = self.canvas.create_rectangle(self.points[0][0],self.points[0][1],self.points[1][0],self.points[1][1])
			elif(self.flag == "drawPolygon"):
				lineId = ""
				self.points.append([x,y])
				pLen = len(self.points)
				if (pLen == 1):
					self.pointId = self.drawPoint([x,y])
				elif (pLen==2):
					self.canvas.delete(self.pointId)
					lineId = self.canvas.create_line(self.points[pLen-2][0],self.points[pLen-2][1],x,y)
					self.lineIds.append(lineId)
				else:
					lineId = self.canvas.create_line(self.points[pLen-2][0],self.points[pLen-2][1],x,y)
					self.lineIds.append(lineId)



root = Tk()
root.resizable(width=FALSE, height=FALSE)
app = App(root)
root.mainloop()
		





