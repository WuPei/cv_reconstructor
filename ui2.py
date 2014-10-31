from Tkinter import *
from PIL import Image, ImageTk

class App:
	def __init__(self, master):
		self.master = master
		self.master.title("cv_recontruction")
		
		self.initUI()
		self.clear()
		
	def initUI(self):
		#load image use PIL library
		self.img = Image.open("project.jpeg")
		angle = 180
		tkImage = ImageTk.PhotoImage(self.img.rotate(180))
		
		#top bar frame
		topFrame = Frame(self.master,width =self.img.size[0]+20,height = 30)
		topFrame.pack()
		topFrame.pack_propagate(0)

		#optionMenu
		variable = StringVar(self.master)
		variable.set("cylinder") # default value

		self.optionMenu = OptionMenu(topFrame, variable, "cylinder","cuboid","prism","frustum","tree","earth","sky")
		self.newShapeButton = Button(topFrame,text = "create new shape",command = self.newShapeButton)

		"""
		self.newCylinderButton = Button(topFrame,text = "newCylinder",commmand = self.newCylinderButton)
		self.newCuboidButton = Button(topFrame,text = "newCuboid",commmand = self.newCuboidButton)
		self.newPrismButton = Button(topFrame,text = "newPrism",commmand = self.newPrismButton)
		self.newFrustumButton = Button(topFrame,text = "newFrustum",commmand = self.newFrustumButton)
		self.newTreeButton = Button(topFrame,text = "newTree",commmand = self.newTreeButton)
		self.earthButton = Button(topFrame,text = "earth",commmand = self.earthButton)
		self.skyButton = Button(topFrame,text = "sky",commmand = self.skyButton)
		"""
		self.rectangleButton = Button(topFrame,text="rectangle",command = self.rectangleButton)
		self.polygonButton = Button(topFrame,text="polygon",command = self.polygonButton)
		self.circleButton = Button(topFrame,text="circle",command = self.polygonButton)
		
		self.doneButton = Button(topFrame,text = "done",command = self.doneButton)
		self.cancelButton = Button(topFrame,text = "cancel",command = self.cancelButton)
		self.showTopFrame("init")

		#frame of canvas + scroll bar
		frame = Frame(self.master)
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

	def showTopFrame(self,state):
		if (state == "init"):
			self.optionMenu.pack(side = LEFT)
			self.newShapeButton.pack(side = LEFT)
			
			self.rectangleButton.pack_forget()
			self.polygonButton.pack_forget()
			self.circleButton.pack_forget()
			
			self.doneButton.pack_forget()
			self.cancelButton.pack_forget()
		elif (state == "second"):
			self.optionMenu.pack_forget()
			self.newShapeButton.pack_forget()
			
			self.rectangleButton.pack(side = LEFT)
			self.polygonButton.pack(side = LEFT)
			self.circleButton.pack(side = LEFT)
			
			self.doneButton.pack_forget()
			self.cancelButton.pack_forget()
		elif (state == "draw"):
			self.optionMenu.pack_forget()
			self.newShapeButton.pack_forget()
			
			self.rectangleButton.pack_forget()
			self.polygonButton.pack_forget()
			self.circleButton.pack_forget()
			
			self.doneButton.pack(side = LEFT)
			self.cancelButton.pack(side = LEFT)
	def clear(self):
		self.flag = ""
		self.pointId = ""
		self.drawId = ""
		self.points =[]
		self.models = []
		self.lineIds = []
	def newShapeButton(self):
		self.showTopFrame("second")
	def rectangleButton(self):
		self.showTopFrame("draw")
		self.flag = "drawRect"
	def circleButton(self):
		self.showTopFrame("draw")
		self.flag = "drawCircle"
	def polygonButton(self):
		self.showTopFrame("draw")
		self.flag = "drawPolygon"
	def cancelButton(self):
		if self.flag == "drawRect":
			self.canvas.delete(self.drawID)
		elif self.flag == "drawPolygon":
			for x in xrange(len(self.lineIds)):
				self.canvas.delete(self.lineIds[x])
		self.clear()
		self.showTopFrame("init")
	def doneButton(self):
		self.clear()
		self.showTopFrame("init")
	def drawPoint(self,p):
		return self.canvas.create_oval(p[0],p[1],p[0],p[1])
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
		





