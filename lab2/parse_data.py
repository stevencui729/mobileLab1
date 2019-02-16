import os
import json

def parse_data_file(filepath, pos= False):
    """
    return list of dictionaries, each dictionary representing data for a particular MAC address
    """
    with open(filepath, 'r') as f:
        loaded_file_string = f.read().replace("'", '"')
        loaded_raw_data = json.loads(loaded_file_string)

    MAC_A = "f8:cf:c5:97:e0:9e"
    MAC_B = "ec:d0:9f:db:e8:1f"
    MAC_C = "80:e6:50:1b:a7:80"
    MAC_GROUND = "44:91:60:d3:d6:94"
    mac_data = {MAC_A: {}, MAC_B: {}, MAC_C: {}, MAC_GROUND: {}}

    for data_line in loaded_raw_data:
        mac = data_line["mac"]
        loc_x = data_line["loc_x"]
        loc_y = data_line["loc_y"]
        if pos:
            rss = abs(int(data_line["rss"]))
        else:
            rss = int(data_line["rss"])
        if mac == MAC_A:
            mac_data[MAC_A][(loc_y, loc_x)] = rss
        elif mac == MAC_B:
            mac_data[MAC_B][(loc_y, loc_x)] = rss
        elif mac == MAC_C:
            mac_data[MAC_C][(loc_y, loc_x)] = rss
        elif mac == MAC_GROUND:
            mac_data[MAC_GROUND][(loc_y, loc_x)] = rss
        else:
            print("Error: unexpected MAC address")
            print(mac)
            return -1

    return mac_data

def fetch_abs_paths(directory):
    """
    return list of absolute filepaths for all files in given directory
    """
    filepaths = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            filepaths.append(os.path.abspath(os.path.join(dirpath, f)))
    return filepaths

def parse_data_directory(directory, pos= False):
    """
    for all rss data files in given directory
    return list of dictionaries, each dictionary containing data for a particular MAC address
    """
    MAC_A = "f8:cf:c5:97:e0:9e"
    MAC_B = "ec:d0:9f:db:e8:1f"
    MAC_C = "80:e6:50:1b:a7:80"
    MAC_GROUND = "44:91:60:d3:d6:94"
    dir_mac_data = {MAC_A: {}, MAC_B: {}, MAC_C: {}, MAC_GROUND: {}}

    filepaths = fetch_abs_paths(directory)

    for filepath in filepaths:
        file_mac_data = parse_data_file(filepath, pos)
        dir_mac_data[MAC_A].update(file_mac_data[MAC_A])
        dir_mac_data[MAC_B].update(file_mac_data[MAC_B])
        dir_mac_data[MAC_C].update(file_mac_data[MAC_C])
        dir_mac_data[MAC_GROUND].update(file_mac_data[MAC_GROUND])
    #flippedData = flipData(dir_mac_data)
    return dir_mac_data

def flipData(data):
    for macAddr in data.keys():
        maxRSS = 0
        for point in data[macAddr].keys():
            if data[macAddr][point] > maxRSS:
                maxRSS = data[macAddr][point]
        for point in data[macAddr].keys():
            data[macAddr][point] = maxRSS - data[macAddr][point]
    return data

def view_summary_stats(directory):
    directory_data = parse_data_directory(directory)

    for key, dict in directory_data.items():
        print("Statistics for MAC : " + key)
        x_values = []
        y_values = []
        for tuple, rss in dict.items():
            x_values.append(tuple[0])
            y_values.append(tuple[1])
        print("Min x: ", min(x_values))
        print("Max x: ", max(x_values))
        print("Mean x: ", (sum(x_values)/len(x_values)))
        print("Min y: ", min(y_values))
        print("Max y: ", max(y_values))
        print("Mean y: ", (sum(y_values)/len(y_values)))
    

def main():
    pass
    #macs = parse_data_file("final_lab2_data/rss-1522970318.944313.txt")
    #macs = parse_data_file("final_lab2_data/rss-1522970573.742740.txt")
    # directory_data = parse_data_directory("final_lab2_data")
    # view_summary_stats("final_lab2_data")

if __name__ == "__main__":
    main()
