import numpy as np
import cv2

class recolor:
    def __init__(self):
        self.colorPicked = (0,0,0)
        self.pick = False
        self.imgShape = None
        self.image = None
        
    def pickColor(self, filename):
        image = cv2.imread(filename)
        self.image = image
        greybar = np.zeros((60, image.shape[1], 3), np.uint8)
        greybar.fill(187)
        self.imgShape = image.shape

        for r in range(7, 54):
            for c in range(7, 54):
                greybar[r,c] = (0,0,0)
        cv2.putText(greybar, "Pick a colour! Then press ENTER to confirm", (70,35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 25)
        
        def getBGRAtMouse(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                bgr = display[y,x]
                if y < self.imgShape[0]:
                    self.colorPicked = bgr
                    self.pick = True

        while True:
            if cv2.getWindowProperty('window-name', 0) < 0:
                cv2.namedWindow('images')
                cv2.setMouseCallback('images', getBGRAtMouse)
                display = np.vstack([image, greybar])
                
            if self.pick:
                for r in range(7, 54):
                    for c in range(7, 54):
                        greybar[r,c] = self.colorPicked
                display = np.vstack([image, greybar])
                self.pick = False
                
            cv2.imshow("images", display)
            k = cv2.waitKey(10)
            if k == 13:  # PRESS ENTER TO CONFIRM COLOUR
                break
        cv2.destroyAllWindows()
        print "Colour picked:", self.colorPicked

    def changeColor(self, set1, set2):
        r = set1  # defines the range of color 
        hue = set2  # defines the change in hue
        print "Range:", r
        print "Hue:", hue 
        
        lower = [0,0,0]
        upper = [0,0,0]
        for i in range(3):
            if self.colorPicked[i] - r < 0:
                lower[i] = 0
            else:
                lower[i] = self.colorPicked[i] - r
            if self.colorPicked[i] + r > 255:
                upper[i] = 255
            else:
                upper[i] = self.colorPicked[i] + r
        print "Lower:", lower
        print "Upper:", upper

        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        mask = cv2.inRange(self.image, lower, upper)
        extract = cv2.bitwise_and(self.image, self.image, mask = mask)

        '''
        display = np.hstack([image, extract])
        while True:    
            cv2.imshow("images", display)
            k = cv2.waitKey(0)
            if k == 27 or cv2.getWindowProperty('window-name', 0) < 0:
                break
        cv2.destroyAllWindows()
        '''

        img_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        img_h, img_s, img_v = cv2.split(img_hsv)
        ext_b, ext_g, ext_r = cv2.split(extract)
        row,col = mask.shape

        for r in range(row):
            for c in range(col):
                if not (ext_b[r,c] == 0 and ext_g[r,c] == 0 and ext_r[r,c] == 0):
                    if hue >= 180:
                        hue -= 180
                    img_h[r,c] = hue

        img_hsv = cv2.merge((img_h, img_s, img_v))
        output = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

        def getBGRAtMouse(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                bgr = display[y,x]
                print "({}\t{}):\t[{}\t{}\t  {}]".format(x, y, bgr[0], bgr[1], bgr[2])

        cv2.namedWindow('images')
        cv2.setMouseCallback('images', getBGRAtMouse)
        display = np.hstack([self.image, output])
        while True:    
            cv2.imshow("images", display)
            k = cv2.waitKey(0)
            if k == 27 or cv2.getWindowProperty('window-name', 0) < 0:
                break
        cv2.destroyAllWindows()

if __name__ == '__main__':
    rc = recolor()
    rc.pickColor("test.jpg")
    rc.changeColor(80, 40)
