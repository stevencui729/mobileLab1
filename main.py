import parse_data as pd
import generateFeatures as gf
import pprint as pp
import sys

def find_bounds(full_data):
    activity_bounds = {}
    for activity in full_data:
        cur_traces = full_data[activity]
        var_bounds = {'minX': sys.maxsize, 'maxX': -1, 'minY': sys.maxsize,
            'maxY': -1, 'minZ': sys.maxsize, 'maxZ': -1}

        for trace in cur_traces:
            varDict = gf.generateFeatures(trace)[0]
            for direction in varDict:
                dir_max_key = 'max'+direction[0].upper()
                dir_min_key = 'min'+direction[0].upper()
                if varDict[direction] < var_bounds[dir_min_key]:
                    var_bounds[dir_min_key] = varDict[direction]
                if varDict[direction] > var_bounds[dir_max_key]:
                    var_bounds[dir_max_key] = varDict[direction]

        activity_bounds[activity] = var_bounds
    return activity_bounds


def classify_activity(trace):
    classified_activity = None
    varDict, powerSpectrums, spectrumPeaks, relTime = gf.generateFeatures(trace)
    varZ = varDict['zAccl']
    if (varZ / 100000) > 0:
        print("varZ less than 6 digits, identified as jumping")
        classified_activity = "Jumping"
    elif varZ < 5000:
        print("varZ less 5000, identified as jumping")
        classified_activity = "Standing"
    else: 




def main():
    parsed_data = pd.parse_data()
    bounds = find_bounds(parsed_data)
    pp.pprint(bounds)
    # first_walking_trace = parsed_data['Walking'][0]
    # first_driving_trace = parsed_data['Driving'][0]
    # first_standing_trace = parsed_data['Standing'][0]
    # first_jumping_trace = parsed_data['Jumping'][0]
    # classify_activity(first_walking_trace)

if __name__ == "__main__":
    main()