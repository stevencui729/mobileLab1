import parse_data as pd
import generateFeatures as gf
import pprint as pp
import os
import sys


def classify_activity(trace):
    classified_activity = None
    varDict, powerSpectrums, midPowers, relTime = gf.generateFeatures(trace)
    varZ = varDict['zAccl']
    midPowerZ = midPowers['zAccl']
    if varZ > 300000:
        print("varZ is: "+str(varZ)+" - greater than 300,000, identified as jumping")
        classified_activity = "Jumping"
    elif varZ < 5000:
        print("varZ is: "+str(varZ)+" - less than 5,000, identified as standing")
        classified_activity = "Standing"
    elif midPowerZ > 0.2:
        print("midPowerZ is: "+str(midPowerZ)+" - greater than 0.2, identified as driving")
        classified_activity = "Driving"
    else:
        print("midPowerZ is: "+str(midPowerZ)+" - less than 0.2, identified as walking")
        classified_activity = "Walking"
    return classified_activity


def main():
    # parsed_data = pd.parse_data_train()

    # # playing arounds with bounds finder
    # # bounds = find_bounds(parsed_data)
    # # pp.pprint(bounds)

    # # test running classifier on all the training data
    # for activity in parsed_data:
    #     print(activity)
    #     cur_traces = parsed_data[activity]

    #     for trace in cur_traces:
    #         classify_activity(trace)


    # running classifier on test data
    parsed_data = pd.parse_data_test()
    for trace in parsed_data:
        print(trace)
        cur_trace = parsed_data[trace]
        classify_activity(cur_trace)

if __name__ == "__main__":
    main()