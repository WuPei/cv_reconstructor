from Tkinter import *
from PIL import Image, ImageTk

class App:
	def __init__(self, master):
		self.master = master
		self.master.title("cv_recontruction")

		#self.shapes = []
		
		self.initUI()
		self.clear()
		
	def initUI(self):
		self.initTopFrames()
		self.initLeftFrame()
		self.initRightFrames()

		#show topframe 1 and right frame
		self.showTopFrame(1)
		self.showRightFrame(1)
		

	#pragma mark -- init frames
	def initTopFrames(self):
		#top frame 1
		self.topFrame1 = Frame(self.master,width =1000+20, height = 30, bd=1, relief=SUNKEN)

		self.shape = StringVar(self.master)
		self.shape.set("cylinder") # default value
		self.shapeOptionMenu = OptionMenu(self.topFrame1, self.shape, "cylinder","cuboid","prism","frustum","tree","earth","sky")
		
		self.newShapeButton = Button(self.topFrame1, text = "create new shape",command = self.newShapeButton)

		#top frame 2
		self.topFrame2 = Frame(self.master,width =1000+20, height = 30, bd=1, relief=SUNKEN)

		self.face = StringVar(self.master)
		self.face.set("Rectangle") # default value
		self.faceOptionMenu = OptionMenu(self.topFrame2, self.face, "rectangle","circle","polygon")
		
		self.addFaceButton = Button(self.topFrame2, text = "add new face",command = self.addFaceButton)

		#top frame 3
		self.topFrame3 = Frame(self.master,width =1000+20, height = 30, bd=1, relief=SUNKEN)

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
		self.canvas = Canvas(self.leftFrame, width = 1000+20, height = 600+20,xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)
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
		self.shapesList = Listbox(self.rightFrame1)
		self.shapesList.insert(END, "a shapes entry")
		for item in ["one", "two", "three", "four"]:
			self.shapesList.insert(END, item)

		self.rightFrame2 = Frame(self.master,width =250, height =600+20+30, bd=1, relief=SUNKEN)
		self.cancelButton2 = Button(self.rightFrame2, text = "cancel",command = self.cancelButton2)
		self.doneButton2 = Button(self.rightFrame2, text = "done", command = self.doneButton2)

		self.rightFrame3 = Frame(self.master,width =250, height =600+20+30, bd=1, relief=SUNKEN)
		self.faceDirLabel = Label(self.rightFrame3, text="Orientation: ")
		self.faceDirEntry = Entry(self.rightFrame3)

	#pragma mark -- show frames
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
			self.shapesList.pack(fill= BOTH)
		else:
			self.rightFrame1.grid_forget()
			self.shapesList.pack_forget()

	def showRightFrame2(self,flag):
		if flag == 1:
			self.rightFrame2.grid(column=1, row =0,  rowspan = 2, sticky=N+W+E+S)
			self.rightFrame2.grid_propagate(0)
			self.doneButton2.grid(column=0,row = 0)
			self.cancelButton2.grid( column = 0, row =1)

			shape = self.shape.get()
			if shape == "cylinder":
				print "1"
			elif shape == "cuboid":
				print "1"
			elif shape == "prism":
				print "1"
			elif shape == "frustum":
				print "1"
			elif shape == "tree":
				print "1"
			elif shape == "ground":
				print "1"
			elif shape == "sky":
				print "1"

		else:
			self.rightFrame2.grid_forget()
			self.doneButton2.grid_forget()
			self.cancelButton2.grid_forget()

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

	def clear(self):
		self.flag = ""
		self.pointId = ""
		self.drawId = ""
		self.points =[]
		self.models = []
		self.lineIds = []


	#pragma mark -- button actions
	def newShapeButton(self):
		self.showTopFrame(2)
		self.showRightFrame(2)

	def addFaceButton(self):
		self.showTopFrame(3)
		self.showRightFrame(3)

	def cancelButton2(self):
		self.showTopFrame(1)
		self.showRightFrame(1)

	def doneButton2(self):
		self.showTopFrame(1)
		self.showRightFrame(1)

	def cancelButton3(self):
		self.showTopFrame(2)
		self.showRightFrame(2)

	def doneButton3(self):
		self.showTopFrame(2)
		self.showRightFrame(2)

	#pragma mark -- click event	
	def canvasClicked(self,event):
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
app = App(root)
root.mainloop()
		





