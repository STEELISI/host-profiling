import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator
import numpy as np
import argparse
import profile_analysis as pf_a

def paint(out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix):

    fig, ax = plt.subplots()
    
    # initialize x 
    # 24*12 = 288
    x_out_service = np.arange(-0.5, 288, 1)
    x_out_noservice = np.arange(-0.5, 288, 1)
    x_in_service = np.arange(-0.5, 288, 1)
    x_in_noservice = np.arange(-0.5, 288, 1)

    out_service_port_num = len(normalized_out_service_matrix)
    y_out_service = np.arange(-0.5, out_service_port_num, 1)
    Z_out_service = np.array(normalized_out_service_matrix)

    ax.pcolormesh(x_out_service, y_out_service, Z_out_service, cmap='binary', vmin=0, vmax=1)

    out_noservice_port_num = len(normalized_out_noservice_matrix)
    # errors here 
    y_out_noservice = np.arange(-1.5, out_noservice_port_num, -1)
    Z_out_noservice = np.array(normalized_out_noservice_matrix)

    ax.pcolormesh(x_out_noservice, y_out_noservice, Z_out_noservice, cmap='binary', vmin=0, vmax=1)

    plt.show()

if __name__ == "__main__":
    print("Visualizing ......")
    out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix = pf_a.generate_normalized_profile_martix("results/8.17_profile_results.txt", "65.89.253.157", 2)

    paint(out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix)