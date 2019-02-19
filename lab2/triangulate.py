import numpy as np 
from tqdm import tqdm
import parse_data
import math
from math import sqrt, isnan
import csv
import cmath
import pandas as pd
import postprocess
import sys
import pickle
import matplotlib.pyplot as plt

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
            stat_writer.writerow([Origin, Error, N])
        
def hipassfilter(data, threshold):
    pointlist = list(data.keys())
    max = 0
    min = np.inf
    for point in pointlist:
        print(data[point])

    1/0
    return pointlist

def triangulateSource(data, p1idx = 0, threshold=.2, log = False):
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
            theta = (A.T@A).I@A.T@b
            originCandidate = (theta.item(0), theta.item(1))
            residual = 0
            power1 = rss2power(data[point1][0])
            dist1 = pointDist(point1, originCandidate)
            for point in pointList[1:]:
                partialError = dist1/pointDist(point, originCandidate)
                partialError = partialError - (rss2power(data[point][0])/power1)**(1/n)
                partialError = partialError ** 2
                # residual = residual + partialError
                residual = residual + (data[point][1] ** 2) * partialError
            if residual < bestError:
                bestError = residual
                bestOrigin = originCandidate
                bestN = n
            if log:
                stat_writer.writerow([originCandidate, residual, n])
    return (bestOrigin, bestError, bestN)

def rss2power(rss):
    power = 10**((rss)/10)
    return power

def generateA(data, pointList, n):
    point1 = pointList[0]
    AList = []
    normPower1 = rss2power(data[point1][0])**(2/n)
    normPower1X = normPower1*point1[0]
    normPower1Y = normPower1*point1[1]
    for point in pointList[1:]:
        normPower2 =rss2power(data[point][0])**(2/n)
        elm1 = 2*(normPower2*point[0] - normPower1X)
        elm2 = 2*(normPower2*point[1] - normPower1Y)
        elm3 = normPower1 - normPower2
        AList.append([elm1, elm2, elm3])
    return np.matrix(AList)

def generateb(data, pointList, n):
    point1 = pointList[0]
    bList = []
    RHS = (rss2power(data[point1][0])**(2/n)) * (point1[0]**2+ point1[1]**2)
    for point in pointList[1:]:
        LHS = (rss2power(data[point][0])**(2/n)) *(point[0]**2+ point[1]**2)
        bList.append([LHS-RHS])
    return np.matrix(bList)

        

def main():
    macs = ["44:91:60:d3:d6:94", "80:e6:50:1b:a7:80", "ec:d0:9f:db:e8:1f", "f8:cf:c5:97:e0:9e"]
    # # initialize custom points test dictionary
    # new_dict = {(10.0, 10.2): (-40.0, 1.0),
    #             (10.3, 10.1): (-40.0, 1.0),
    #             (102.1, 101.0): (-75.0, 1.0),
    #             (100.0, 100.0): (-75.0, 1.0)}
    #             # (10.0, 100,0): -50.0}

    # filter method testing
    test_data = parse_data.parse_data_directory("./final_lab2_data")
    dfs = postprocess.data_to_dfs(test_data)
    full_dfs = [pd.concat(postprocess.split_mac_to_lines(dfs[mac]).values()) for mac in macs]
    # full_df = pd.concat(postprocess.split_mac_to_lines(dfs["44:91:60:d3:d6:94"]).values())
    # full_df = pd.concat(postprocess.split_mac_to_lines(dfs["80:e6:50:1b:a7:80"]).values())
    # full_df = pd.concat(postprocess.split_mac_to_lines(dfs["ec:d0:9f:db:e8:1f"]).values())
    # full_df = pd.concat(postprocess.split_mac_to_lines(dfs["f8:cf:c5:97:e0:9e"]).values())
    for full_df in full_dfs:
        df = postprocess.normalize_rss(full_df) # ground truth
        high_confs = postprocess.select_high_confs(df)
        df = df[(df['nscore'] > 0.9) | ((df['nscore'] > 0.1) & (df['nscore'] < 0.2))]

        # adding high confidence points to selected
        # df = pd.concat([df, high_confs])
        # df = postprocess.normalize_rss(df)

        # using high confidence points only
        # df = high_confs
        # df = postprocess.normalize_rss(df)

        new_dict = {}
        for i, row in df.iterrows():
            new_dict[(row['x'], row['y'])] = (row['rss'], row['nscore'])
        print("after initial 0.9 cleaning: "+str(len(new_dict.keys())))

        origin, error, n = triangulateSource(new_dict, log = True)
        print(origin, error, n)
        fig, ax = postprocess.visualize({"44:91:60:d3:d6:94": new_dict})
        ax.scatter([-22],[162], c="green")
        ax.scatter([origin[0]],[origin[1]], c="blue")
        plt.show()

    # change first point testing
    # for i, data in enumerate([groundSet, set1, set2, set3]):
    #     origin, error, n = triangulateSource(data, log = True)
    #     print(i)
    #     print("Origin:", origin)
    #     print("error:", error)
    #     print("N", n)
    #changePoint1(groundSet, 10)

if __name__ == "__main__":
    main()