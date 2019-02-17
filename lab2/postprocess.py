import json
import pprint as pp
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib as mp
import parse_data
import pandas as pd
from tqdm import tqdm

import sys

floorplan_runs = {
    "A12": {"xstart": 72, "ystart": 249, "xend": 120, "yend": 165},
    "A23": {"xstart": 120, "ystart": 165, "xend": 12, "yend": 165},
    "A31": {"xstart": 12, "ystart": 165, "xend": 72, "yend": 249},
    "B12": {"xstart": 72, "ystart": 129, "xend": 72, "yend": 21},
    "B23": {"xstart": 72, "ystart": 21, "xend": 228, "yend": 21},
    "B31": {"xstart": 228, "ystart": 21, "xend": 72, "yend": 129},
    "C12": {"xstart": 168, "ystart": 261, "xend": 289, "yend": 261},
    "C23": {"xstart": 289, "ystart": 261, "xend": 289, "yend": 201},
    "C31": {"xstart": 289, "ystart": 201, "xend": 168, "yend": 261} 
}

def visualize(data):
    for key in data:
        # cur_mac_data = data[key]
        # num_vals = len(cur_mac_data.keys())
        # sorted_points = sorted(cur_mac_data.keys())

        # x_vals = np.empty(num_vals)
        # y_vals = np.empty(num_vals)
        # rss_vals = np.empty(num_vals)

        # for i, point in enumerate(sorted_points):
            # print(i, point, cur_mac_data[point])
            # x_vals[i] = point[0]
            # y_vals[i] = point[1]
            # rss_vals[i] = cur_mac_data[point]

        
        x = data[key]['x']
        y = data[key]['y']
        rss = data[key]['rss']
        cmap = cm.get_cmap('Reds')
        normalize = mp.colors.Normalize(vmin=min(rss), vmax=max(rss))
        colors = [cmap(normalize(value)) for value in rss]

        fig, ax = plt.subplots(figsize=(10,10))
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(key)
        plt.scatter(x, y, s=1, c=rss, cmap=cmap)
        # plotting ground truth and other point
        # if key == '44:91:60:d3:d6:94':
        plt.scatter([-22],[162], c="blue")
        plt.scatter([143],[175], c="green")
            

        cax, _ = mp.colorbar.make_axes(ax)
        cbar = mp.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
        # plt.savefig("fig_"+key+".jpeg", dpi=500)
        plt.show()


def data_to_dfs(data):
    dfs = {}
    for key in data:
        cur_mac_data = data[key]
        num_vals = len(cur_mac_data.keys())
        sorted_points = sorted(cur_mac_data.keys())

        x_vals = np.empty(num_vals)
        y_vals = np.empty(num_vals)
        rss_vals = np.empty(num_vals)

        for i, point in enumerate(sorted_points):
            # print(i, point, cur_mac_data[point])
            x_vals[i] = point[0]
            y_vals[i] = point[1]
            rss_vals[i] = cur_mac_data[point]

        cur_df = pd.DataFrame({'x': x_vals, 'y': y_vals, 'rss': rss_vals})
        dfs[key] = cur_df
    return dfs


def sliding_window_clean(dfs):
    win_size = 5
    for key in dfs:
        cur_df = dfs[key]
        num_vals = cur_df.shape[0]
        indices_to_remove = []
        for i in tqdm(range(num_vals)):
            x_val = cur_df['x'][i]
            y_val = cur_df['y'][i]
            logical_window = (cur_df['x'] < x_val+win_size/2) & \
                (cur_df['x'] > x_val-win_size/2) & \
                (cur_df['y'] < y_val+win_size/2) & \
                (cur_df['y'] > y_val-win_size/2)
            
            # log number matching
            # unique, counts = np.unique(logical_window, return_counts=True)
            # print(dict(zip(unique, counts)))

            in_window = cur_df[logical_window]
            #Q1 = in_window['rss'].quantile(0.25)
            #Q3 = in_window['rss'].quantile(0.75)
            Q1 = in_window['rss'].quantile(0.1)
            Q3 = in_window['rss'].quantile(0.6)
            IQR = Q3 - Q1
            to_remove = in_window[(in_window['rss'] < (Q1 - 1.5 * IQR)) | (in_window['rss'] > (Q3 + 1.5 * IQR))]
            indices_to_remove.extend(to_remove.index.values)
            
        indices_to_remove = set(indices_to_remove)
        cleaned_cur_df = cur_df.drop(indices_to_remove)
        print(cleaned_cur_df.shape)
        pickle_path = key+"_winsize"+str(win_size)+"_pickle"
        cleaned_cur_df.to_pickle(pickle_path)


def pickle_to_old_format(file_path):
    df = pd.read_pickle(file_path)
    new_dict = {}
    for i, row in df.iterrows():
        new_dict[(row['x'], row['y'])] = row['rss']
    return new_dict


def apply_kalman(split_dfs):
    sys.path.append('./kalmanjs/contrib/python/')
    import kalman
    KFilter = kalman.KalmanFilter(0.008, 0.1)
    for run in split_dfs:
        cur_df = split_dfs[run]
        num_vals = cur_df.shape[0]
        for i, row in cur_df.iterrows():
            row['rss'] = KFilter.filter(row['rss'])
    full_df = pd.concat(split_dfs.values())
    print(full_df.shape)
    return full_df


def split_mac_to_lines(mac_df):
    split_dfs = {}
    for run in floorplan_runs:
        print(run)
        endpoints = floorplan_runs[run]
        if endpoints['xstart'] < endpoints['xend']:
            xwindow = (mac_df['x'] > endpoints['xstart']) & \
                (mac_df['x'] < endpoints['xend'])
        else:
            xwindow = (mac_df['x'] <= endpoints['xstart']) & \
                (mac_df['x'] >= endpoints['xend'])
        
        if endpoints['ystart'] < endpoints['yend']:
            ywindow = (mac_df['y'] > endpoints['ystart']) & \
                (mac_df['y'] < endpoints['yend'])
        else:
            ywindow = (mac_df['y'] <= endpoints['ystart']) & \
                (mac_df['y'] >= endpoints['yend'])
        logical_window = xwindow & ywindow
            
        # log number matching
        # unique, counts = np.unique(logical_window, return_counts=True)
        # print(dict(zip(unique, counts)))
        in_window = mac_df[logical_window] 
        print(in_window.shape)
        split_dfs[run] = in_window
    return split_dfs

def main():
    print("hi")
    test_data = parse_data.parse_data_directory("./final_lab2_data")
    dfs = data_to_dfs(test_data)
    split_dfs = split_mac_to_lines(dfs["44:91:60:d3:d6:94"])
    all_dfs = apply_kalman(split_dfs)
    # new_dict = {}
    # for i, row in df.iterrows():
    #     new_dict[(row['x'], row['y'])] = row['rss']
    # print(all_dfs)
    visualize({"44:91:60:d3:d6:94": all_dfs})


    # sliding_window_clean(dfs)
    # old_format_pickle = pickle_to_old_format("./44:91:60:d3:d6:94_pickle")
    # visualize(test_data)


if __name__ == "__main__":
    main()