import json
import pprint as pp
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib as mp


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

        cmap = cm.get_cmap('Reds_r')
        normalize = mp.colors.Normalize(vmin=min(rss_vals), vmax=max(rss_vals))
        colors = [cmap(normalize(value)) for value in rss_vals]
        fig, ax = plt.subplots(figsize=(10,10))
        ax.scatter(x_vals, y_vals, color=colors)
        cax, _ = mp.colorbar.make_axes(ax)
        cbar = mp.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
        fig = plt.scatter(x_vals, y_vals, c=rss_vals, cmap=cmap)
        
        plt.show()


def gen_test_data():
    rss1 = -40
    rss2 = -20
    rss3 = -50
    rss4 = -100
    full_dict = {'mac1': {(0, 0): rss1, (0, 50): rss2, (50, 0): rss3, (50, 50): rss4}}
    return full_dict


def main():
    print("hi")
    test_data = gen_test_data()
    visualize(test_data)


if __name__ == "__main__":
    main()