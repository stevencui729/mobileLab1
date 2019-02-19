import os
import json
import pandas as pd
import numpy as np
import sys


def read_tracefile(path):
    with open(path, 'r') as f:
        loaded_file_string = f.read().replace("'", '"')
        loaded_raw_data = json.loads(loaded_file_string)

    new_frame = pd.DataFrame(columns=['x', 'y', 'rss', 'mac'])
    for i, data_line in enumerate(loaded_raw_data):
        new_frame.loc[i]= [data_line["loc_y"], data_line["loc_x"], int(data_line['rss']), data_line["mac"]]
    rss = new_frame['rss']
    # print(rss.mean())
    print(min(rss), max(rss), np.mean(rss), np.median(rss), np.std(rss))

def read_car_mappings(path):
    mappings = {}
    with open(path, "rb") as f:
        for line in f.readlines():
            linesplit = line.split()
            mappings[linesplit[1]] = linesplit[0]
    return mappings
    
def main():
    dirlist = os.listdir('./final_lab2_data')
    # print(dirlist)
    # for trace in dirlist:
    #     read_tracefile('./final_lab2_data/'+trace)
    mappings = read_car_mappings('./car_traces.txt')
    print(mappings)
    

if __name__ == "__main__":
    main()