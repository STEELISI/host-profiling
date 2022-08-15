import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator
import numpy as np
import argparse
import profile_analysis as pf_a

def paint(out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix):

    # fig, ax = plt.subplots()
    fig, axs = plt.subplots(2, 1)
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

    axs[0].pcolormesh(x_out_service, y_out_service, Z_out_service, cmap='binary', vmin=0, vmax=1)
    _frame(axs[0], x_out_service, y_out_service)

    out_noservice_port_num = len(normalized_out_noservice_matrix)
    y_out_noservice = np.arange(-1.5, -out_noservice_port_num-2, -1)
    Z_out_noservice = np.array(normalized_out_noservice_matrix)

    axs[0].pcolormesh(x_out_noservice, y_out_noservice, Z_out_noservice, cmap='binary', vmin=0, vmax=1)
    _frame(axs[0], x_out_noservice, y_out_noservice)

    # draw inbound traffic
    in_service_port_num = len(normalized_in_service_matrix)
    y_in_service = np.arange(-0.5, in_service_port_num, 1)
    Z_in_service = np.array(normalized_in_service_matrix)

    axs[1].pcolormesh(x_in_service, y_in_service, Z_in_service, cmap='binary', vmin=0, vmax=1)
    _frame(axs[1], x_in_service, y_in_service)

    in_noservice_port_num = len(normalized_in_noservice_matrix)
    y_in_noservice = np.arange(-1.5, -in_noservice_port_num-2, -1)
    Z_in_noservice = np.array(normalized_in_noservice_matrix)

    axs[1].pcolormesh(x_in_noservice, y_in_noservice, Z_in_noservice, cmap='binary', vmin=0, vmax=1)
    _frame(axs[1], x_in_noservice, y_in_noservice)

    plt.show()

if __name__ == "__main__":
    print("Visualizing ......")
    out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix = pf_a.generate_normalized_profile_martix("results/8.17_profile_results.txt", "65.89.253.157", 2)

    paint(out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix)