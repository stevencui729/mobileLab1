import os
import json

work_dir = os.path.join(os.getcwd(), "activity-trainingdata")

def parse_file(filepath):
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


def parse_data():
    parsed_data = {}
    for filename in os.listdir(work_dir):
        filepath = os.path.join(work_dir, filename)
        print("parsing file: "+filepath)
        curData = parse_file(filepath)
        parsed_data[curData[0]['activity']] = curData 
    
    return parsed_data

if __name__ == "__main__":
    data = parse_data()
    print(len(data.keys()))