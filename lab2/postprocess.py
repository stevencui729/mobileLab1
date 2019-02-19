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
        # dictionary methods
        cur_mac_data = data[key]
        num_vals = len(cur_mac_data.keys())
        sorted_points = sorted(cur_mac_data.keys())

        x = np.empty(num_vals)
        y = np.empty(num_vals)
        rss = np.empty(num_vals)

        for i, point in enumerate(sorted_points):
            x[i] = point[0]
            y[i] = point[1]
            rss[i] = cur_mac_data[point][0]

        # DataFrame methods
        # x = data[key]['x']
        # y = data[key]['y']
        # rss = data[key]['rss']

        cmap = cm.get_cmap('Reds')
        normalize = mp.colors.Normalize(vmin=-110, vmax=0)
        colors = [cmap(normalize(value)) for value in rss]

        fig, ax = plt.subplots(figsize=(10,10))
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(key)
        plt.scatter(x, y, c=colors, cmap=cmap)
            
        cax, _ = mp.colorbar.make_axes(ax)
        cbar = mp.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
        # plt.savefig("fig_"+key+".jpeg", dpi=500)
    return fig, ax


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


def apply_kalman(split_dfs):
    sys.path.append('./kalmanjs/contrib/python/')
    import kalman
    for run in split_dfs:
        KFilter = kalman.KalmanFilter(0.008, 0.1)
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
            
        in_window = mac_df[logical_window] 
        in_window['run'] = run
        split_dfs[run] = in_window
    return split_dfs


def summary_stats_on_runs(split_dfs):
    for run in split_dfs:
        cur_df = split_dfs[run]
        print(run)
        print(max(cur_df['rss']), min(cur_df['rss']), np.median(cur_df['rss']), np.std(cur_df['rss']))        


def normalize_rss(df):
    nscores = (df['rss'] - min(df['rss'])) / (max(df['rss']) - min(df['rss']))
    df['old_rss'] = df['rss']
    df['nscore'] = nscores
    df['rss'] = (1 - nscores) * -110
    return df

def select_high_confs(df):
    runs = set(floorplan_runs.keys())
    selected_points = []
    for run in runs:
        window = (df['run'] == run)
        in_window = df[window] 
        selected_points.append(in_window.nlargest(1, 'nscore'))
    return pd.concat(selected_points)

def main():
    print("hi, my name is process. post process")

    # tag by leg and normalize test
    test_data = parse_data.parse_data_directory("./final_lab2_data")
    dfs = data_to_dfs(test_data)
    full_df= pd.concat(split_mac_to_lines(dfs["44:91:60:d3:d6:94"]).values())
    df = normalize_rss(full_df)
    select_high_confs(df)

    # applying kalman test
    # all_dfs = apply_kalman(split_dfs)

    # visualize test
    # new_dict = {}
    # for i, row in df.iterrows():
    #     new_dict[(row['x'], row['y'])] = (row['rss'], row['nscore'])
    # print(all_dfs)
    # visualize({"44:91:60:d3:d6:94": all_dfs})

    # sliding window test
    # sliding_window_clean(dfs)
    # old_format_pickle = pickle_to_old_format("./44:91:60:d3:d6:94_pickle")
    # visualize(test_data)


if __name__ == "__main__":
    main()