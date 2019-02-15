import numpy as np 
from tqdm import tqdm
import parse_data

def triangulateSource(data):
    pointList = list(data.keys())
    bestN = 0
    bestError = np.inf
    for n in np.arange(1, 5, .05):
        A = generateA(data, n)
        print(len(pointList))
        print(A.shape)
        1/0
        b = generateb(data)
        theta = (A.T*A).I*A.T*b

def generateA(data,n):
    pointList = list(data.keys())
    point1 = pointList[0]
    AList = []
    normPower1 = data[point1]**(2/n)
    normPower1X = normPower1*point1[0]
    normPower1Y = normPower1*point1[1]
    for point in pointList[1:]:
        normPower2 =data[point]**(2/n)
        elm1 = 2*(normPower2*point[0] - normPower1X)
        elm2 = 2*(normPower2*point[1] - normPower1Y)
        elm3 = normPower1 - normPower2
        AList.append([elm1, elm2, elm3])
    return np.matrix(AList)
        

def main():
    print("henlo")
    data = parse_data.parse_data_directory("./final_lab2_data")
    MAClist = list(data.keys())
    triangulateSource(data[MAClist[0]])
    pass

if __name__ == "__main__":
    main()