import sys
import os
import time
import math
import numpy as np
from PIL import Image

start_time = time.time()

class MyImage:
    def __init__(self, path, mode, folderName):
        self.realImage = np.array(Image.open(path, ).convert('RGB'), dtype='int')
        self.height, self.width, self.colors = self.realImage.shape
        self.energyMatrix = np.empty([self.height, self.width])
        self.seamImage = np.empty([self.height, self.width, 3], dtype='int')

        self.seamCoordinates = []
        self.mark = np.ones((self.height, self.width), dtype=np.bool)

        self.mode = mode

        self.folderName = folderName

    
    def getPixelRGB(self, x, y):
        return self.realImage[x, y]

    def getPixelEnergy(self, x, y):
        if x == 0:
            leftPixelRGB = (0, 0, 0)
        else:
            leftPixelRGB = self.getPixelRGB(x - 1, y)

        if x == self.height - 1:
            rightPixelRGB = (0, 0, 0)
        else:
            rightPixelRGB = self.getPixelRGB(x + 1, y)

        if y == 0:
            bottomPixelRGB = (0, 0, 0)
        else:
            bottomPixelRGB = self.getPixelRGB(x, y - 1)
        
        if y == self.width - 1:
            topPixelRGB = (0, 0, 0)
        else:
            topPixelRGB = self.getPixelRGB(x, y + 1)
        
        Rx = rightPixelRGB[0] - leftPixelRGB[0]
        Gx = rightPixelRGB[1] - leftPixelRGB[1]
        Bx = rightPixelRGB[2] - leftPixelRGB[2]
        xDeltaSquare = Rx ** 2 + Gx ** 2 + Bx ** 2

        Ry = topPixelRGB[0] - bottomPixelRGB[0]
        Gy = topPixelRGB[1] - bottomPixelRGB[1]
        By = topPixelRGB[2] - bottomPixelRGB[2]
        yDeltaSquare = Ry ** 2 + Gy ** 2 + By ** 2

        return math.sqrt(xDeltaSquare + yDeltaSquare)
    
    def updateImageDimension(self):
        self.height, self.width, self.colors = self.realImage.shape
    
    def updateEnergyMatrix(self):
        energyMatrix = np.empty([self.height, self.width])
        for i in range(self.height):
            for j in range(self.width):
                energyMatrix[i][j] = self.getPixelEnergy(i, j) 
        self.energyMatrix = energyMatrix

        # Vectorize Implementation
        # deltaX2 = np.square(np.roll(self.realImage, -1, axis = 0) - np.roll(self.realImage, 1, axis = 0))
        # deltaY2 = np.square(np.roll(self.realImage, -1, axis = 1) - np.roll(self.realImage, 1, axis = 1))
        # self.energyMatrix = np.sum(deltaX2, axis = 2) + np.sum(deltaY2, axis = 2)

    def updateVerticalSeam(self):
        minEnergyMatrix = self.energyMatrix.copy()
        backtrack = np.zeros_like(minEnergyMatrix, dtype=np.int)

        for i in range(1, self.height):
            for j in range(0, self.width):
                if j == 0:
                    index = np.argmin(minEnergyMatrix[i - 1, j:j + 2])
                    backtrack[i, j] = index + j
                    minEnergy = minEnergyMatrix[i - 1, index + j]
                else:
                    index = np.argmin(minEnergyMatrix[i - 1, j - 1:j + 2])
                    backtrack[i, j] = index + j - 1
                    minEnergy = minEnergyMatrix[i - 1, index + j - 1]

                minEnergyMatrix[i, j] += minEnergy
        
        mark = np.ones((self.height, self.width), dtype=np.bool)
        seamPixels = []

        # Find the position of the smallest element in the last row of minEnergyMatrix
        j = np.argmin(minEnergyMatrix[-1])

        # Mark the pixels for deletion
        for i in reversed(range(self.height)):
            seamPixels.append((i, j))
            mark[i, j] = False
            j = backtrack[i, j]
        
        self.seamCoordinates = seamPixels
        self.mark = mark

    def updateSeamImage(self):
        seamImage = np.empty([self.height, self.width, 3], dtype='int')
        maxEnergy = np.amax(self.energyMatrix)
        scale = 255 / maxEnergy
        for i in range(self.height):
            for j in range(self.width):
                # This if can be outside of the two above for loops
                if (i, j) in self.seamCoordinates:
                    seamImage[i][j] = (255, 0, 0)
                else:
                    pixelRGB = scale * self.energyMatrix[i][j]
                    seamImage[i][j] = (pixelRGB, pixelRGB, pixelRGB)
        self.seamImage = seamImage
    
    def updateAll(self):
        self.updateImageDimension()
        self.updateEnergyMatrix()
        self.updateVerticalSeam()
        self.updateSeamImage()

    def deleteVerticalSeam(self):
        mark = np.stack([self.mark] * 3, axis=2)
        self.realImage = self.realImage[mark].reshape((self.height, self.width - 1, 3))
        if self.mode == "time":
            self.energyMatrix = self.energyMatrix[self.mark].reshape((self.height, self.width - 1))
    
    def saveSeamImage(self, index):
        array = self.seamImage.astype(np.uint8)
        image = Image.fromarray(array)
        path = '../Result/' + str(self.folderName)
        if not os.path.exists(path):
            os.makedirs(path)
        image.save(path + '/Seam' + index + '.png')
    
    def saveRealImage(self):
        array = self.realImage.astype(np.uint8)
        image = Image.fromarray(array)
        path = '../Result/' + str(self.folderName)
        if not os.path.exists(path):
            os.makedirs(path)
        image.save(path + '/Final.png')

    def removeColumns(self, columns):
        for i in range(columns):
            self.updateAll()
            self.saveSeamImage('_col' + str(i))
            self.deleteVerticalSeam()
            

    def removeRows(self, rows):
        if rows <= 0:
            return

        self.realImage = np.rot90(self.realImage, 1, (0, 1))
        for i in range(rows):
            self.updateAll()
            self.seamImage = np.rot90(self.seamImage, 3, (0, 1))
            self.saveSeamImage('_row' + str(i))
            self.deleteVerticalSeam()

        self.realImage = np.rot90(self.realImage, 3, (0, 1))

    def remove(self, columns, rows):
        if self.mode == "quality":
            self.removeColumns(columns)
            self.removeRows(rows)
            self.saveRealImage()
        
        elif self.mode == "time":
            if columns > 0:
                self.updateEnergyMatrix()
                for i in range(columns):
                    self.updateImageDimension()
                    self.updateVerticalSeam()
                    if i == 0:
                        self.updateSeamImage()
                        self.saveSeamImage("")
                    self.deleteVerticalSeam()
                if rows > 0:
                    self.realImage = np.rot90(self.realImage, 1, (0, 1))
                    self.updateImageDimension()
                    self.updateEnergyMatrix()
                    for i in range(rows):
                        self.updateImageDimension()
                        self.updateVerticalSeam()
                        self.deleteVerticalSeam()
                    self.realImage = np.rot90(self.realImage, 3, (0, 1))
            else:
                if rows > 0:
                    self.realImage = np.rot90(self.realImage, 1, (0, 1))
                    self.updateImageDimension()
                    self.updateEnergyMatrix()
                    
                    for i in range(rows):
                        self.updateImageDimension()
                        self.updateVerticalSeam()
                        if i == 0:
                            self.updateSeamImage()
                            self.seamImage = np.rot90(self.seamImage, 3, (0, 1))
                            self.saveSeamImage("")
                        
                        self.deleteVerticalSeam()
                        
                    self.realImage = np.rot90(self.realImage, 3, (0, 1))
            self.saveRealImage()

if __name__ == "__main__":
    path = sys.argv[1]
    cols = int(sys.argv[2])
    rows = int(sys.argv[3])
    mode = sys.argv[4]
    export_folder_name = sys.argv[5]

    image = MyImage(path, mode, export_folder_name)
    image.remove(cols, rows)

print("--- %s seconds ---" % (time.time() - start_time))