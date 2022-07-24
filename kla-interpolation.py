import numpy as np
import math
import scipy
from scipy.interpolate import griddata

#Data
waferDiameter = -1
input = []

print("KLA Polar Interpolation:")

#Open file
with open("TiWN batch reactor uniformity.fimap") as f:
    contents = f.readlines()

#Read data from file (diameter and points)
currentLine = 0
for line in contents[:len(contents)-7]:
    currentLine += 1
    if "Wafer Dia" in line:
        waferDiameter = int(line[line.find(',')+1:])
        print(f"Wafer Diameter: {line[line.find(',')+1:]}")
    if currentLine >= 27:
        firstComma = line.find(',')
        secondComma = line[firstComma+1:].find(',')+firstComma+1
        thirdComma = line[secondComma+1:].find(',')+secondComma+1
        x = line[:firstComma]
        y = line[firstComma+1:secondComma]
        z = line[secondComma+1:thirdComma]
        if z == "-1":
            currentLine -= 1
        else:
            input.append([float(x),float(y),float(z)])
            #print([float(x),float(y),float(z)])

data = np.transpose(np.asarray(input))

#Calculate spacing
scalar = 0.05
spacing = scalar*math.sqrt(np.pi*waferDiameter**2/2/np.size(data))

newx = np.arange(-waferDiameter/2-spacing, waferDiameter/2+spacing, spacing)
newy = np.arange(-waferDiameter/2-spacing, waferDiameter/2+spacing, spacing)
gridx, gridy = np.meshgrid(newx,newy)

#Define number of columns and rows
numcols = np.size(gridx,1)
numrows = np.size(gridx,0)

gridx = gridx.flatten()
gridy = gridy.flatten()

#Interpolate data to cartesian grid
interpolationMethod = 'linear'
datai = scipy.interpolate.griddata((data[0],data[1]), data[2], (gridx, gridy), method=interpolationMethod, fill_value=0)
#datai = np.nan_to_num(datai)
values = np.transpose(datai.reshape(numrows, numcols))

#Output file for ProfilmOnline
with open(f"reactor_{scalar}_{interpolationMethod}.txt", 'w') as f:
    f.write(f"{'numCols'}\t{'numRows'}\t{'pixelSize'}\n")
    f.write(f"{numcols}\t{numrows}\t{spacing}\n")
    f.write(f"{'Z-data'}\n")
    for row in values:
        for value in row:
            f.write(f"{value}\t")
        f.write("\n")

    f.write(f"{'RGB-data'}\n{'imageType'}\t{'bytesPerPixel'}\n")
    f.write(f"{0}\t{1}\n")
    for row in values:
        for point in row:
            f.write(f"{0}\t")
        f.write("\n")
