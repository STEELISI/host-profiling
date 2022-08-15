from fileinput import filename
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import utilities as ut
import os
import random
import copy

def select_n_randomly(n, from_file, to_file):
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

def clustering(file):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    spf_dict = ut.dict_read_from_file(filename)

    print(spf_dict)


if __name__ == "__main__":
    # select_n_randomly(100, "results/8.17_simplified_profile_results.txt", "sampled_100_simplified_profile.txt")
    clustering("sampled_100_simplified_profile.txt")
