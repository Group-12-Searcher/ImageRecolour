import numpy as np
import cv2
import Tkinter as tk
#root = tk.Tk()

class recolor:
    def __init__(self, screen_width, screen_height):
        self.screenWidth = screen_width
        self.screenHeight = screen_height
        self.selectingRegion = False
        self.regionStart = (0,0)
        self.regionEnd = None
        self.colorPicked = (0,0,0)
        self.huePicked = 0
        self.pick = False
        self.image = None
        self.imgShape = None
        self.regionDisplay = None

    def selectRegion(self, filename):
        self.image = cv2.imread(filename)
        self.imgShape = self.image.shape
        self.regionStart = (0,0)
        
        print "Image Size:", self.imgShape
        print "Screen Size:", self.screenWidth, self.screenHeight
        if self.imgShape[0] > self.screenHeight-135:
            self.image = cv2.resize(self.image, (self.imgShape[1], self.screenHeight-135))
        if self.imgShape[1] > self.screenWidth:
            self.image = cv2.resize(self.image, (self.screenWidth, self.imgShape[0]))
        self.imgShape = self.image.shape

        self.regionDisplay = self.image.copy()
        self.regionEnd = (self.imgShape[1]-1, self.imgShape[0]-1)
        row, col, cha = self.imgShape
        
        greybar = np.zeros((80, self.imgShape[1], 3), np.uint8)
        greybar.fill(187)
        cv2.putText(greybar, "Click & drag to select a region!", (7,22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 15)
        cv2.putText(greybar, "Then press ENTER to confirm", (7,47), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 15)
        
        def drawRegion(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.selectingRegion = True
                if x < 0: x = 0
                if x > self.imgShape[1]-1: x = self.imgShape[1]-1
                if y < 0: y = 0
                if y > self.imgShape[0]-1: y = self.imgShape[0]-1
                self.regionStart = (x,y)            
                    
            if self.selectingRegion:
                self.regionDisplay = self.image.copy()
                if x < 0: x = 0
                if x > self.imgShape[1]-1: x = self.imgShape[1]-1
                if y < 0: y = 0
                if y > self.imgShape[0]-1: y = self.imgShape[0]-1
                self.regionEnd = (x,y)
                cv2.rectangle(self.regionDisplay, self.regionStart, self.regionEnd, (0, 255, 0), 2)

            if event == cv2.EVENT_LBUTTONUP:
                self.selectingRegion = False

        while True:
            if cv2.getWindowProperty('window-name', 0) < 0:
                cv2.namedWindow('Draw Region')
                cv2.setMouseCallback('Draw Region', drawRegion)
                cv2.moveWindow('Draw Region', 0, 0)
                #cv2.setWindowProperty('Draw Region', cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_NORMAL);
                display = np.vstack([self.regionDisplay, greybar])
            elif self.selectingRegion:
                display = np.vstack([self.regionDisplay, greybar])
                
            cv2.imshow('Draw Region', display)
            k = cv2.waitKey(10)
            if k == 13:  # PRESS ENTER TO CONFIRM COLOUR
                break
        cv2.destroyAllWindows()
        
        x1,x2,y1,y2 = self.regionStart[0], self.regionEnd[0], self.regionStart[1], self.regionEnd[1]
        if x1 > x2:
            temp = x1
            x1 = x2
            x2 = temp
        if y1 > y2:
            temp = y1
            y1 = y2
            y2 = temp
        self.regionStart = (x1,y1)
        self.regionEnd = (x2,y2)
        print "Region selected:", self.regionStart, ",", self.regionEnd

        regionDisplayHSV = cv2.cvtColor(self.regionDisplay, cv2.COLOR_BGR2HSV)
        for r in range(row):
            for c in range(col):
                if c < self.regionStart[0] or r < self.regionStart[1] or c > self.regionEnd[0] or r > self.regionEnd[1]:
                    v = regionDisplayHSV[r,c,2]
                    v -= 100
                    if v < 0: v = 0
                    regionDisplayHSV[r,c,2] = v

        self.regionDisplay = cv2.cvtColor(regionDisplayHSV, cv2.COLOR_HSV2BGR)
        self.pickColor()
            
    def pickColor(self):
        greybar = np.zeros((60, self.imgShape[1], 3), np.uint8)
        greybar.fill(187)

        for r in range(7, 54):
            for c in range(7, 54):
                greybar[r,c] = (0,0,0)
                cv2.putText(greybar, "Pick a colour from the region!", (62,25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 15)
        cv2.putText(greybar, "Then press ENTER to confirm", (62,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 15)
        
        def getColourAtMouse(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                pixel = display[y:y+1,x:x+1]
                if y < self.imgShape[0] and x > self.regionStart[0]+1 and x < self.regionEnd[0]-1 and y > self.regionStart[1]+1 and y < self.regionEnd[1]-1:
                    self.colorPicked = pixel[0,0]
                    self.huePicked = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)[0,0,0]
                    self.pick = True

        while True:
            if cv2.getWindowProperty('window-name', 0) < 0:
                cv2.namedWindow('Pick Colour')
                cv2.setMouseCallback('Pick Colour', getColourAtMouse)
                cv2.moveWindow('Pick Colour', 0, 0)
                display = np.vstack([self.regionDisplay, greybar])
                
            if self.pick:
                for r in range(7, 54):
                    for c in range(7, 54):
                        greybar[r,c] = self.colorPicked
                display = np.vstack([self.regionDisplay, greybar])
                self.pick = False
                
            cv2.imshow("Pick Colour", display)
            k = cv2.waitKey(10)
            if k == 13:  # PRESS ENTER TO CONFIRM COLOUR
                break
        cv2.destroyAllWindows()
        
        print "Colour picked:", self.colorPicked
        print "Hue picked:", self.huePicked
        
    
    def changeColor(self, set1, set2):
        rng = set1
        newHue = set2 / 2.0
        hueChange = newHue - self.huePicked
        print "Recolour range:", rng
        print "Change in hue:", hueChange
        
        lower = [0,0,0]
        upper = [0,0,0]
        for i in range(3):
            if self.colorPicked[i] - rng < 0:
                lower[i] = 0
            else:
                lower[i] = self.colorPicked[i] - rng
            if self.colorPicked[i] + rng > 255:
                upper[i] = 255
            else:
                upper[i] = self.colorPicked[i] + rng
        print "Lower:", lower
        print "Upper:", upper

        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        mask = cv2.inRange(self.image, lower, upper)
        extract = cv2.bitwise_and(self.image, self.image, mask = mask)

        '''
        display = np.hstack([self.image, extract])
        while True:    
            cv2.imshow("images", display)
            k = cv2.waitKey(0)
            if k == 27 or cv2.getWindowProperty('window-name', 0) < 0:
                break
        cv2.destroyAllWindows()
        '''

        img_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        row,col = mask.shape

        for r in range(self.regionStart[1]+1, self.regionEnd[1]):
            for c in range(self.regionStart[0]+1, self.regionEnd[0]):
                if not (extract[r,c,0] == 0 and extract[r,c,1] == 0 and extract[r,c,2] == 0):
                    hue = img_hsv[r,c,0]
                    hue += hueChange
                    if hue < 0 or hue >= 180:
                        hue = hue % 180
                    img_hsv[r,c,0] = hue

        output = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

        def getColourAtMouse(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                pixel = display[y:y+1,x:x+1]
                bgr = pixel[0,0]
                hue = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)[0,0,0]
                print "coor({},{}):\tBGR[{},{},{}]\tHue({})".format(x, y, bgr[0], bgr[1], bgr[2], hue)

        if self.imgShape[1] > self.screenWidth/2:
            imageCopy = cv2.resize(self.image, (self.screenWidth/2, self.imgShape[0]))
            output = cv2.resize(output, (self.screenWidth/2, self.imgShape[0]))
        else:
            imageCopy = self.image
        
        cv2.namedWindow('Result')
        cv2.setMouseCallback('Result', getColourAtMouse)
        cv2.moveWindow('Result', 0, 0)
        display = np.hstack([imageCopy, output])
        while True:    
            cv2.imshow("Result", display)
            k = cv2.waitKey(0)
            if k == 27 or cv2.getWindowProperty('window-name', 0) < 0:
                break
        cv2.destroyAllWindows()

if __name__ == '__main__':
    rc = recolor()
    rc.pickColor("butterfly.jpg")
    rc.changeColor(110, 270)
