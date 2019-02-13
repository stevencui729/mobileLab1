import os
import json


def parse_file_train(filepath):
    with open(filepath, 'r') as f:
        loaded_file_string = f.read().replace("'", '"')
        loaded_raw_data = json.loads(loaded_file_string)

    data_points = []
    for trace in loaded_raw_data:
        try:
            activity_name = trace['type']
        except KeyError:
            activity_name = None
            print("could not find activity, setting `activity_name` to None")
        
        data_seq = trace['seq']
        xList = [data_point['data']['xAccl'] for data_point in data_seq]
        yList = [data_point['data']['yAccl'] for data_point in data_seq]
        zList = [data_point['data']['zAccl'] for data_point in data_seq]
        timeList = [data_point['time'] for data_point in data_seq]

        parsed_dict = {"xAccl": xList, "yAccl": yList, "zAccl": zList, 
            "time": timeList, "activity": activity_name}
        data_points.append(parsed_dict)
    
    return data_points


def parse_data_train():
    work_dir = os.path.join(os.getcwd(), "activity-trainingdata")
    parsed_data = {}
    for filename in os.listdir(work_dir):
        filepath = os.path.join(work_dir, filename)
        print("parsing file: "+filepath)
        curData = parse_file_train(filepath)
        parsed_data[curData[0]['activity']] = curData 
    
    return parsed_data

def parse_file_test(filepath):
    with open(filepath, 'r') as f:
        loaded_file_string = f.read().replace("'", '"')
        loaded_raw_data = json.loads(loaded_file_string)

    try:
        activity_name = loaded_raw_data['type']
    except KeyError:
        activity_name = None
        print("could not find activity, setting `activity_name` to None")
    
    data_seq = loaded_raw_data['seq']
    xList = [data_point['data']['xAccl'] for data_point in data_seq]
    yList = [data_point['data']['yAccl'] for data_point in data_seq]
    zList = [data_point['data']['zAccl'] for data_point in data_seq]
    timeList = [data_point['time'] for data_point in data_seq]
    parsed_dict = {"xAccl": xList, "yAccl": yList, "zAccl": zList, 
        "time": timeList, "activity": activity_name}
    
    return parsed_dict

def parse_data_test():
    work_dir = os.path.join(os.getcwd(), "activity-test-dataset")
    parsed_data = {}
    for filename in os.listdir(work_dir):
        filepath = os.path.join(work_dir, filename)
        print("parsing file: "+filepath)
        curData = parse_file_test(filepath)
        parsed_data[filename] = curData 
    
    return parsed_data