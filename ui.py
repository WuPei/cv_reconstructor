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
        
        #create canvas to load the image
        canvas = Canvas(master, width = img.size[0]+20 , height = img.size[1]+20)
        canvas.create_image(10, 10,anchor=NW, image=tkImage)
        canvas.image = tkImage      #hold a reference
        canvas.pack(fill = BOTH, expand = 1)




root = Tk()
app = App(root)
root.mainloop()
#root.destroy() # optional; see description below