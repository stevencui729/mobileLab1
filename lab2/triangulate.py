import numpy as np 
from tqdm import tqdm
import parse_data
import math
from math import sqrt, isnan

def pointDist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2  )

def triangulateSource(data):
    pointList = list(data.keys())
    point1 = pointList[0]
    bestN = 0
    bestError = np.inf
    bestOrigin = (0,0)
    for n in np.arange(1, 5, .05):
        A = generateA(data, pointList, n)
        b = generateb(data, pointList, n)
        theta = (A.T*A).I*A.T*b
        originCandidate = (theta.item(0), theta.item(1))
        residual = 0
        power1 = data[point1]
        dist1 = pointDist(point1, originCandidate)
        print(originCandidate)
        for point in pointList[1:]:
            partialError = dist1/pointDist(point, originCandidate)
            partialError = partialError - (data[point]/power1)**(1/n)
            partialError = partialError ** 2
            residual = residual +  partialError
        if residual < bestError:
            bestError = residual
            bestOrigin = originCandidate
            bestN = n
        return (bestOrigin, bestError, bestN)



def generateA(data, pointList, n):
    point1 = pointList[0]
    AList = []
    normPower1 = math.pow(data[point1],(2/n))
    normPower1X = normPower1*point1[0]
    normPower1Y = normPower1*point1[1]
    for point in pointList[1:]:
        normPower2 =data[point]**(2/n)
        elm1 = 2*(normPower2*point[0] - normPower1X)
        elm2 = 2*(normPower2*point[1] - normPower1Y)
        elm3 = normPower1 - normPower2
        AList.append([elm1, elm2, elm3])
    return np.matrix(AList)

def generateb(data, pointList, n):
    point1 = pointList[0]
    bList = []
    RHS = data[point1]**(2/n) *(point1[0]**2+ point1[1]**2)
    for point in pointList[1:]:
        LHS = data[point]**(2/n) *(point[0]**2+ point[1]**2)
        bList.append([LHS-RHS])
    return np.matrix(bList)

        

def main():
    print("henlo")
    data = parse_data.parse_data_directory("./final_lab2_data")
    MAClist = list(data.keys())
    print(MAClist[3])
    origin, error, n = triangulateSource(data[MAClist[3]])
    print("Origin:", origin)
    print("error:", error)
    print("N", n)

if __name__ == "__main__":
    main()