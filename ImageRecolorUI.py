from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox
import tkFileDialog
import recolor

class ImageRecolorUI(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
         
        self.parent = parent
        self.supportedFormats = ["jpg", "png"]
        self.colorRange = IntVar()
        self.hueValue = IntVar()
        self.hasPreviousQuery = False
        
        self.initUI()

    def initUI(self):
      
        self.parent.title("ImageRecolor")
        self.centerAppWindow()
        self.loadUploadButton()
        self.loadRegionSelectionButton()

        
    def centerAppWindow(self):
        # geometry in the form of width x height + x_offset + y_offset
        # x_offset: +ve = move right, y_offset: move down
        width = 500
        height = 500
        x_offset = (self.parent.winfo_screenwidth() - width) / 2
        y_offset = (self.parent.winfo_screenheight() - height) / 2
        self.parent.geometry("%dx%d+%d+%d" % (width, height, x_offset, y_offset))

    def loadUploadButton(self):
        uploadButton = Button(self.parent, text="Upload image", command=self.uploadImage)
        uploadButton.pack()
        separator = Label(self.parent)
        separator.pack()

    def loadRegionSelectionButton(self):
        regionButton = Button(self.parent, text="Select region", command=self.drawRegion)
        regionButton.pack()
        separator = Label(self.parent)
        separator.pack()

    def uploadImage(self):
        if (self.hasPreviousQuery):
            self.imagePanel.pack_forget()
            self.unloadInputs()
            
        self.imageURL = tkFileDialog.askopenfilename()
        #print(self.imageURL.split("/")[-1].split("."))
        if self.imageURL.split("/")[-1].split(".")[1] not in self.supportedFormats:
            tkMessageBox.showerror("Invalid File Format", "Please upload a JPG or PNG image.")
        else:
            uploadedImg = Image.open(self.imageURL)
            uploadedImg = uploadedImg.resize((250, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(uploadedImg)
            self.imagePanel = Label(self.parent, image=img)
            self.imagePanel.image = img
            self.imagePanel.pack()
            self.loadInputs()
            self.hasPreviousQuery = True

    def drawRegion(self):
        # invoke backend program and pass image URL to it
        print("Drawing region for %s" % self.imageURL)
        recolor.pickColor(self.imageURL)

    def loadInputs(self):
        self.colorRangeLabel = Label(self.parent, text="Specify color range amount: ")
        self.colorRangeLabel.pack()
        self.colorRangeEntry = Entry(self.parent, textvariable=self.colorRange)
        self.colorRangeEntry.pack()
        self.colorHueLabel = Label(self.parent, text="Specify color hue amount between [0, 359]: ")
        self.colorHueLabel.pack()
        self.colorHueEntry = Entry(self.parent, textvariable=self.hueValue)
        self.colorHueEntry.pack()
        self.submitButton = Button(self.parent, text="Submit", command=self.submitInputs)
        self.submitButton.pack()

    def unloadInputs(self):
        self.colorRangeLabel.pack_forget()
        self.colorRangeEntry.pack_forget()
        self.colorHueLabel.pack_forget()
        self.colorHueEntry.pack_forget()
        self.submitButton.pack_forget()

    def submitInputs(self):
        # send user inputs to backend program
        print("Color range specified: " + str(self.colorRange.get()))
        print("Hue value specified: " + str(self.hueValue.get()))
        recolor.changeColor(self.colorRange, self.hueValue)

def main():
  
    root = Tk()
    app = ImageRecolorUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
