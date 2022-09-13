# Yebo Feng 

import os
import utilities as ut

def separate_(file):
    # print the first n elements in the profile dictionary

    

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)


    for i, (k, v) in enumerate(pf_dict.items()):

if __name__ == "__main__":
    print("running")