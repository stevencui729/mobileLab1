import json
import pprint as pp
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib as mp
import parse_data


def visualize(data):
    for key in data:
        cur_mac_data = data[key]
        num_vals = len(cur_mac_data.keys())

        x_vals = np.empty(num_vals)
        y_vals = np.empty(num_vals)
        rss_vals = np.empty(num_vals)

        for i, (point, rss_val) in enumerate(cur_mac_data.items()):
            # print(i, point, rss_val)
            x_vals[i] = point[0]
            y_vals[i] = point[1]
            rss_vals[i] = rss_val

        # y and x are currently flipped due to errors in their shit
        cmap = cm.get_cmap('Reds_r')
        normalize = mp.colors.Normalize(vmin=min(rss_vals), vmax=max(rss_vals))
        colors = [cmap(normalize(value)) for value in rss_vals]
        fig, ax = plt.subplots(figsize=(10,10))
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(key)
        ax.scatter(y_vals, x_vals, color=colors)
        cax, _ = mp.colorbar.make_axes(ax)
        cbar = mp.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
        fig = plt.scatter(y_vals, x_vals, c=rss_vals, cmap=cmap)
        plt.savefig("fig_"+key+".jpeg")


def main():
    print("hi")
    test_data = parse_data.parse_data_directory("./final_lab2_data")
    visualize(test_data)


if __name__ == "__main__":
    main()