# Yebo Feng 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import utilities as ut
import os
import random
import copy
import pickle
from sklearn.cluster import AgglomerativeClustering
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import numpy as np
from joblib import dump, load

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

def select_n_sp_randomly(n, from_file, to_file):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, from_file)
    spf_dict = ut.dict_read_from_file(filename)

    spf_dict_key = list(spf_dict.keys())
    new_dict = dict()
    sampled_spf_dict_key = random.sample(spf_dict_key, n)
    for ip in sampled_spf_dict_key:
        temp_dict = dict()
        temp_dict = copy.deepcopy(spf_dict[ip][2])
        new_dict[ip] = dict()
        for i, (k, v) in enumerate(temp_dict.items()):
            new_dict[ip][k] = v[1]
    
    to_dirname = os.path.dirname(__file__)
    filename_write = os.path.join(to_dirname, to_file)
    ut.dict_write_to_file(new_dict, filename_write)

def select_n_bidirectional_sp_randomly(n, from_file, to_file):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, from_file)
    spf_dict = ut.dict_read_from_file(filename)

    spf_dict_key = list(spf_dict.keys())
    new_dict = dict()

    num = 0
    while num <= n:
        ip = random.choice(spf_dict_key)
        if ip in new_dict:
            continue
        if spf_dict[ip][1][1] >= 100 and spf_dict[ip][1][3] >= 100:
            num += 1
            temp_dict = dict()
            temp_dict = copy.deepcopy(spf_dict[ip][2])
            new_dict[ip] = dict()
            for i, (k, v) in enumerate(temp_dict.items()):
                new_dict[ip][k] = v[1]
        else:
            continue
    
    to_dirname = os.path.dirname(__file__)
    filename_write = os.path.join(to_dirname, to_file)
    ut.dict_write_to_file(new_dict, filename_write)

def select_n_ip_randomly(n, from_file, to_file):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, from_file)
    ip_list = ut.read_list_from_file_linebyline(filename)

    res_list = random.choices(ip_list, k = n)
    to_filename = os.path.join(dirname, to_file)
    ut.save_list_to_file_linebyline(res_list, to_filename)

def clustering_seaborn(file):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    spf_dict = ut.dict_read_from_file(filename)

    dataset = pd.DataFrame.from_dict({i: spf_dict[i] 
                           for i in spf_dict.keys() 
                           }, orient='index')
    dataset = dataset.fillna(0)

    print(dataset)

    samples_of_interest = ['Outbound|443|https', "Outbound|---|NON_SERVICE_PORT", "Inbound|---|NON_SERVICE_PORT", "Inbound|443|https", "Inbound|80|http"]
    sample_labels = [i if i in samples_of_interest else None for i in dataset.columns]

    g = sns.clustermap(dataset, metric="correlation",
    cmap = 'binary',
    xticklabels=sample_labels,
    )
    # plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)

    # plt.show()

    plt.savefig('hierarchical_clustered_heatmap_with_Seaborn_clustermap_python_1st_try.pdf')

def clustering(ip_file, spf_file):
    print("Reading data from files......")
    dirname = os.path.dirname(__file__)
    ip_filename = os.path.join(dirname, ip_file)
    spf_filename = os.path.join(dirname, spf_file)

    ip_list = ut.read_list_from_file_linebyline(ip_filename)
    spf_dict = ut.dict_read_from_file(spf_filename)

    # print(len(ip_list))

    input_data = dict()
    count = 0
    for ip in ip_list:
        # count +=1
        # print(count)
        temp_dict = dict()
        temp_dict = copy.deepcopy(spf_dict[ip][2])
        input_data[ip] = dict()
        for i, (k, v) in enumerate(temp_dict.items()):
            input_data[ip][k] = v[1]
    
    print(len(input_data))

    print("Preparing the dataset!")
    dataset = pd.DataFrame.from_dict({i: input_data[i] 
                           for i in input_data.keys() 
                           }, orient='index')
    dataset = dataset.fillna(0)


    model = AgglomerativeClustering(distance_threshold=0, n_clusters=None, affinity = "euclidean")
    print("Start clustering!")
    model.fit(dataset)
    print("Clustering done!")
    print(model)

    dump(model, 'filename.joblib') 

    plt.title("Hierarchical Clustering Dendrogram")
    # plot the top three levels of the dendrogram
    plot_dendrogram(model, truncate_mode="level", p=1000)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.show()



if __name__ == "__main__":
    # select_n_sp_randomly(100, "results/8.17_simplified_profile_results.txt", "sampled_100_simplified_profile.txt")
    # select_n_sp_bidirectional_randomly(100, "results/8.17_simplified_profile_results.txt", "sampled_100_simplified_profile.txt")
    # select_n_ip_randomly(200,"8.17_unrestricted_ip.txt","200_8.17_unrestricted_ip.txt")
    # select_n_ip_randomly(200,"8.17_restricted_ip.txt","200_8.17_restricted_ip.txt")

    # clustering_seaborn("sampled_100_simplified_profile.txt")
    clustering("2000_8.17_unrestricted_ip.txt", "results/8.17_simplified_profile_results.txt")