from Tkinter import *
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        master.title("cv_recontruction")
        
        self.initUI(master)
    
    def initUI(self,master):
        #load image use PIL library
        img = Image.open("project.jpeg")
        angle = 180
        tkImage = ImageTk.PhotoImage(img.rotate(180))
        
        #top bar frame
        topFrame = Frame(master,width =img.size[0]+20,height = 30)
        topFrame.grid(row = 0, column =0)
        topFrame.pack()
        topFrame.pack_propagate(0)
        self.rectangleButton = Button(topFrame,text="rectangle",command = self.rectangleButton)
        self.rectangleButton.grid(sticky = N+W)
        self.rectangleButton.pack(side=LEFT,fill = X)
        

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
        canvas = Canvas(frame, width = img.size[0]+20 , height = img.size[1]+20,xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)
        canvas.create_image(10, 10,anchor=NW, image=tkImage)
        canvas.image = tkImage      #hold a reference
        #canvas.pack(fill = BOTH, expand = 1)
        canvas.grid(row=0, column=0, sticky=N+S+E+W)

        
        #config scroll bar
        canvas.config(scrollregion=canvas.bbox(ALL))
        xscrollbar.config(command=canvas.xview)
        yscrollbar.config(command=canvas.yview)

        frame.pack()
    def rectangleButton(self):
        print "rectangleButton"



root = Tk()
app = App(root)
root.mainloop()
#root.destroy() # optional; see description below