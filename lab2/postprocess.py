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

def visualize(data):
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

        
            
        # # y and x are currently flipped due to error in the writeup
        # cmap = cm.get_cmap('Reds')
        # normalize = mp.colors.Normalize(vmin=min(rss_vals), vmax=max(rss_vals))
        # colors = [cmap(normalize(value)) for value in rss_vals]

        # fig, ax = plt.subplots(figsize=(10,10))
        # plt.xlabel("x")
        # plt.ylabel("y")
        # plt.title(key)
        # plt.scatter(y_vals, x_vals, s=1, c=rss_vals, cmap=cmap)
        # # plotting ground truth and other point
        # if key == '44:91:60:d3:d6:94':
        #     plt.scatter([-22],[162], c="blue")
        #     plt.scatter([143],[175], c="green")
            

        # cax, _ = mp.colorbar.make_axes(ax)
        # cbar = mp.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
        # plt.savefig("fig_"+key+".jpeg", dpi=500)
        # # plt.show()


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
            Q1 = in_window['rss'].quantile(0.25)
            Q3 = in_window['rss'].quantile(0.75)
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


def main():
    print("hi")
    test_data = parse_data.parse_data_directory("./final_lab2_data")
    # dfs = data_to_dfs(test_data)
    # sliding_window_clean(dfs)
    old_format_pickle = pickle_to_old_format("./44:91:60:d3:d6:94_pickle")
    # visualize(test_data)


if __name__ == "__main__":
    main()