import os
import json

def parse_data_file(filepath):
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
    mac_a = {MAC_A: {}}
    mac_b = {MAC_B: {}}
    mac_c = {MAC_C: {}}
    mac_gr = {MAC_GROUND: {}}

    for data_line in loaded_raw_data:
        mac = data_line["mac"]
        loc_x = data_line["loc_x"]
        loc_y = data_line["loc_y"]
        rss = int(data_line["rss"])
        if mac == MAC_A:
            mac_a[MAC_A][(loc_x, loc_y)] = rss
        elif mac == MAC_B:
            mac_b[MAC_B][(loc_x, loc_y)] = rss
        elif mac == MAC_C:
            mac_c[MAC_C][(loc_x, loc_y)] = rss
        elif mac == MAC_GROUND:
            mac_gr[MAC_GROUND][(loc_x, loc_y)] = rss
        else:
            print("Error: unexpected MAC address")
            print(mac)
            return -1

    return [mac_a, mac_b, mac_c, mac_gr]

def fetch_abs_paths(directory):
    """
    return list of absolute filepaths for all files in given directory
    """
    filepaths = []
    for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           filepaths.append(os.path.abspath(os.path.join(dirpath, f)))
    return filepaths

def parse_data_directory(directory):
    """
    for all rss data files in given directory
    return list of dictionaries, each dictionary containing data for a particular MAC address
    """
    MAC_A = "f8:cf:c5:97:e0:9e"
    MAC_B = "ec:d0:9f:db:e8:1f"
    MAC_C = "80:e6:50:1b:a7:80"
    MAC_GROUND = "44:91:60:d3:d6:94"
    mac_a = {MAC_A: {}}
    mac_b = {MAC_B: {}}
    mac_c = {MAC_C: {}}
    mac_gr = {MAC_GROUND: {}}

    filepaths = fetch_abs_paths(directory)

    for filepath in filepaths:
        list_macs = parse_data_file(filepath)
        for mac in list_macs:
            for key, dict in mac.items():
                if key == MAC_A:
                    mac_a[MAC_A].update(dict)
                elif key == MAC_B:
                    mac_b[MAC_B].update(dict)
                elif key == MAC_C:
                    mac_c[MAC_C].update(dict)
                elif key == MAC_GROUND:
                    mac_gr[MAC_GROUND].update(dict)

    return [mac_a, mac_b, mac_c, mac_gr]

def main():
    # macs = parse_data_file("final_lab2_data/rss-1522970318.944313.txt")
    # macs = parse_data_file("final_lab2_data/rss-1522970573.742740.txt")
    list_macs = parse_data_directory("final_lab2_data")
    for mac in list_macs:
        for key, dict in mac.items():
            print(key)
            print(dict)
            # for tuple, rss in dict.items():
            #     print(tuple)
            #     print(rss)

if __name__ == main():
    main()
