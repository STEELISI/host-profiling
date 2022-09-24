import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator
import numpy as np
import argparse
import profile_analysis as pf_a
import os
import utilities as ut

def paint_profile(out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix):

    # fig, ax = plt.subplots()
    
    fig, axs = plt.subplots(2, 1, figsize=(14,7))

    def _frame(ax, x, y):
        # draw the frame of the profile 
        x_min = min(x)
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
        ax.plot([x_min, x_max], [y_max, y_max], color='k')
        ax.plot([x_min, x_max], [y_min, y_min], color='k')
        ax.plot([x_min, x_min], [y_min, y_max], color='k')
        ax.plot([x_max, x_max], [y_min, y_max], color='k')
    
    # initialize x 
    # 24*12 = 288
    x_out_service = np.arange(-0.5, 288, 1)
    x_out_noservice = np.arange(-0.5, 288, 1)
    x_in_service = np.arange(-0.5, 288, 1)
    x_in_noservice = np.arange(-0.5, 288, 1)

    # draw outbound traffic 
    out_service_port_num = len(normalized_out_service_matrix)
    y_out_service = np.arange(-0.5, out_service_port_num, 1)
    Z_out_service = np.array(normalized_out_service_matrix)

    # print(Z_out_service)

    # check if the profile part exisit
    v_min = 0
    v_max = 1
    if len(Z_out_service) != 0:
        axs[0].pcolormesh(x_out_service, y_out_service, Z_out_service, cmap='binary', vmin=v_min, vmax=v_max)
    _frame(axs[0], x_out_service, y_out_service)

    out_noservice_port_num = len(normalized_out_noservice_matrix)
    y_out_noservice = np.arange(-1.5, -out_noservice_port_num-2, -1)
    Z_out_noservice = np.array(normalized_out_noservice_matrix)

    if len(Z_out_noservice) != 0:
        axs[0].pcolormesh(x_out_noservice, y_out_noservice, Z_out_noservice, cmap='binary', vmin=v_min, vmax=v_max)
    _frame(axs[0], x_out_noservice, y_out_noservice)

    # draw inbound traffic
    in_service_port_num = len(normalized_in_service_matrix)
    y_in_service = np.arange(-0.5, in_service_port_num, 1)
    Z_in_service = np.array(normalized_in_service_matrix)

    if len(Z_in_service) != 0:
        axs[1].pcolormesh(x_in_service, y_in_service, Z_in_service, cmap='binary', vmin=v_min, vmax=v_max)
    _frame(axs[1], x_in_service, y_in_service)

    in_noservice_port_num = len(normalized_in_noservice_matrix)
    y_in_noservice = np.arange(-1.5, -in_noservice_port_num-2, -1)
    Z_in_noservice = np.array(normalized_in_noservice_matrix)

    if len(Z_in_noservice) != 0:
        axs[1].pcolormesh(x_in_noservice, y_in_noservice, Z_in_noservice, cmap='binary', vmin=v_min, vmax=v_max)
    _frame(axs[1], x_in_noservice, y_in_noservice)

    plt.show()

def visual_simplified_profile(file, ip):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    spf_dict = pf_dict[ip][2]
    result_list = []
    for i, (k, v) in enumerate(spf_dict.items()):
        temp_list = []
        temp_list.append(k)
        temp_list.append(v[1])
        result_list.append(temp_list)

    # sort the simplified profile from large to small 
    def sort_key(e):
        return e[1]
    result_list.sort(reverse = True, key = sort_key)

    # extract labels and proportion numbers 
    labels = [i[0] for i in result_list]
    proportions = [i[1] for i in result_list]

    # start plotting 
    x = np.arange(len(labels))  # the label locations
    width = 0.5  # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.bar(x, proportions, width, label='Men')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Traffic Proportion')
    # ax.set_title('Title')
    ax.set_xticks(x, labels, rotation = 90)
    ax.set_ylim(0,1)
    # ax.legend()

    ax.bar_label(rects, padding=3, rotation = 90)

    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    print("Visualizing ......")
    # out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix = pf_a.generate_normalized_profile_martix("results/8.18_profile_results.txt", "65.89.253.157", 2)
    # out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix = pf_a.generate_normalized_profile_martix("results/8.18_profile_results.txt", "68.158.58.84", 2)
    # out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix = pf_a.generate_normalized_profile_martix("results/8.18_profile_results.txt", "14.181.124.20", 2)
    # out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix = pf_a.generate_normalized_profile_martix("results/8.18_profile_results.txt", "14.181.126.240", 2)

    # paint_profile(out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix)

    # visual_simplified_profile("results/8.17_simplified_profile_results.txt", "68.158.58.84")
    # visual_simplified_profile("results/8.17_simplified_profile_results.txt", "14.181.124.20")
    visual_simplified_profile("results/8.18_simplified_profile_results.txt", "14.14.129.177")