import numpy as np 
from tqdm import tqdm
import parse_data
import math
from math import sqrt, isnan
import csv
import cmath

def pointDist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2  )

def changePoint1(data, npoints):
    pointList = list(data.keys())
    p1List = np.linspace(0, len(pointList), npoints, endpoint=False)
    with open('varyp1.csv', mode='w') as f:
        stat_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        stat_writer.writerow(["Origin", "Error", "N"])
        for p1idx in tqdm(p1List):
            Origin, Error, N = triangulateSource(data, int(p1idx))
            #print("p1idx = ", int(p1idx))
            #print("\tOrigin, Error, N:",Origin, Error, N)
            stat_writer.writerow([Origin, Error, N])
        
        

def triangulateSource(data, p1idx = 0, log = False):
    pointList = list(data.keys())
    point1 = pointList[0]
    pointList[0] = pointList[p1idx]
    pointList[p1idx] = point1
    point1 = pointList[0]
    bestN = 0
    bestError = np.inf
    bestOrigin = (0,0)
    print("Triangulating....")
    if log == False:
        mode = 'r'
    else:
        mode = 'w'
    with open('Error&N.csv', mode=mode) as f:
        if log:
            stat_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            stat_writer.writerow(["Origin", "Error", "N"])
        for n in tqdm(np.arange(1, 5, .05)):
            A = generateA(data, pointList, n)
            b = generateb(data, pointList, n)
            theta = (A.T*A).I*A.T*b
            originCandidate = (theta.item(0), theta.item(1))
            residual = 0
            power1 = data[point1]
            dist1 = pointDist(point1, originCandidate)
            #print(originCandidate)
            for point in pointList[1:]:
                partialError = dist1/pointDist(point, originCandidate)
                partialError = partialError - (data[point]/power1)**(1/n)
                partialError = partialError ** 2
                residual = residual +  partialError
            if residual < bestError:
                bestError = residual
                bestOrigin = originCandidate
                bestN = n
            if log:
                stat_writer.writerow([originCandidate, residual, n])
    return (bestOrigin, bestError, bestN)

def rss2power(rss):
    power = 10**(rss/10)
    return power

def generateA(data, pointList, n):
    point1 = pointList[0]
    AList = []
    normPower1 = rss2power(data[point1])**(2/n)
    normPower1X = normPower1*point1[0]
    normPower1Y = normPower1*point1[1]
    for point in pointList[1:]:
        normPower2 =rss2power(data[point])**(2/n)
        elm1 = 2*(normPower2*point[0] - normPower1X)
        elm2 = 2*(normPower2*point[1] - normPower1Y)
        elm3 = normPower1 - normPower2
        AList.append([elm1, elm2, elm3])
    return np.matrix(AList)

def generateb(data, pointList, n):
    point1 = pointList[0]
    bList = []
    RHS = rss2power(data[point1])**(2/n) * (point1[0]**2+ point1[1]**2)
    for point in pointList[1:]:
        LHS = rss2power(data[point])**(2/n) *(point[0]**2+ point[1]**2)
        bList.append([LHS-RHS])
    return np.matrix(bList)

        

def main():
    data = parse_data.parse_data_directory("./final_lab2_data", pos=False)
    MAClist = list(data.keys())
    print(MAClist[3])
    origin, error, n = triangulateSource(data[MAClist[3]], log = True)
    print("Origin:", origin)
    print("error:", error)
    print("N", n)
    changePoint1(data[MAClist[3]], 10)

if __name__ == "__main__":
    main()