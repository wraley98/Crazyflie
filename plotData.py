"""
Get Data
William Raley
16 Jan 24

compares and plots data from the crazyflie program.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from openpyxl import load_workbook

stdList = []
meanList = []

def recordData(trueCoords):
  doc = load_workbook('STDData.xlsx')
  sheet = doc.active

  data = [trueCoords[0] , trueCoords[1] , trueCoords[2] , stdList[0] , stdList[1] , stdList[2] , meanList[0] ,meanList[1], meanList[2] , meanList[3] ,stdList[3]]

  sheet.append(data)

  doc.save('STDData.xlsx')

# plots reletive location data overtime cmpared to actual location 

def plotPercentDiffData(x, y , z, pts , yPTS):
    plt.plot(pts, x)
    plt.plot(pts, z)
    
    meanList.append(np.mean(y))
    stdList.append(np.std(y))
    
    plt.xlabel("Reported Data Point")
    plt.ylabel("Percent Difference")
    plt.legend(["x" , "z"])
    plt.title("Percent Difference in Crazyflie Reported Location vs Actual Location (x, z)")
    plt.savefig('timeplot.png')
    plt.clf()

    plt.plot(yPTS, y)

    plt.xlabel("Reported Data Point")
    plt.ylabel("Percent Difference")
    plt.legend(["y"])
    plt.title("Percent Difference in Crazyflie Reported Location vs Actual Location (y)")
    plt.savefig('timeplotY.png')
    plt.clf()

def plotLocationData(coord, clr, list):

    pts = range(len(list))
    plt.plot(pts, list , color = clr)
   
    plt.xlabel("Reported Data Point")
    plt.ylabel(coord + "Location (m)")
    plt.title("Crazyflie Reported Location (" + coord + ")")
    plt.savefig(coord + '.png')
    plt.clf()

# creates histogram
def createHistogram(coord, clr, list):
    
    plt.hist(list, color = clr)
    plt.title("Distribution of Relative %s Location Data Points (Histogram)" % coord)
    plt.xlabel("Reported %s Location (m)" % coord)
    plt.ylabel("Number of Times Reported")
    plt.savefig('histoplot%s.png' % coord)
    plt.clf()

# creates bell curve
def createBellCurve(coord, clr, list):
   
    mean = np.mean(list)

    meanList.append(mean)

    i = 0
    for val in list:
        list[i] = val - mean
        i += 1
  
    std = np.std(list)
    stdList.append(std)
    list.sort()
    curve = norm.pdf(list , 0, std)
    plt.plot(list , curve, color = clr)
    plt.title("Distribution of Relative %s Location Data Points (Gaussian Curve)" % coord)
    plt.xlabel("Reported Normalized %s Location (m)" % coord)
    plt.ylabel("PDF of %s Location" % coord)
    plt.title("Distribution of Relative %s Coord Data Points (Gaussian Curve)\nMean: %f STD: %f" % (coord, mean , std))
    plt.savefig('bellCurve%s.png' % coord)
    plt.clf()

# calls histogram and bell curve functions for each of the coords
def plotDataRel(x, y, z):

    # name of coords
    coords = ['X' , 'Y' , 'Z']
    # name of colors
    clrs = ['blue' , 'green' , 'magenta']
    # list of coords
    lists = [x , y , z]
    # coord counter
    count = 0

    for i in coords:
        createHistogram(i, clrs[count], lists[count])
        createBellCurve(i, clrs[count], lists[count])
        #plotLocationData(i, clrs[count], lists[count])
        count += 1

# compares location data and plots the data
def compareData(cfX, cfY, cfZ, trueCoords , yPath = None , startY = None):
    
    # creates lists for percent difference
    perctDiffX = []
    perctDiffY = []
    perctDiffZ = []

    numPts = list(range(len(cfX)))
    plotDataRel(cfX, cfY, cfZ)

    if yPath != None:
        for x in cfX:

            perctDiffX.append((x - trueCoords[0]) / trueCoords[0] * 100)
       
        for i in range(len(yPath)):
            perctDiffY.append(( cfY[i + startY] - yPath[i]) / yPath[i] * 100)

        for z in cfZ:
            perctDiffZ.append((z - trueCoords[2]) / trueCoords[2] * 100)
        
        numPts = list(range(len(perctDiffX)))
        yPTS = list(range(len(perctDiffY)))
        plotPercentDiffData(perctDiffX, perctDiffY, perctDiffZ , numPts , yPTS)
    
    
    recordData(trueCoords)
    