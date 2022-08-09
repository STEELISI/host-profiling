import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator
import numpy as np
import argparse
import profile_analysis as pf_a

def paint(out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix):
    # np.random.seed(19680801)
    # Z = np.random.rand(6, 10)

    x = np.arange(-0.5, 288, 1)  # len = 11
    number_of_ports = len(normalized_in_noservice_matrix)
    print(number_of_ports)
    y = np.arange(-0.5, number_of_ports, 1)  # len = 7
    Z = np.array(normalized_in_noservice_matrix)
    # newcmp = LinearSegmentedColormap('testCmap', ["#FFFFFF", "#000000"], N=256)
    fig, ax = plt.subplots()
    ax.pcolormesh(x, y, Z, cmap='binary',vmin=0, vmax=1)
    plt.show()

if __name__ == "__main__":
    print("Visualizing ......")
    out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix = pf_a.generate_normalized_profile_martix("results/8.17_profile_results.txt", "65.89.253.157", 2)

    paint(out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix)