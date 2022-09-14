# Yebo Feng 

import os
import utilities as ut

def is_restricted():
    # return 0 if this ip is not restricted
    # return 1 if this ip is restricted
    return 0

def has_bidirectional_traffic():
    # return 0 if does not have bidirectional traffic
    # return 1 if has bidirectional traffic
    return 0

def separate_ip(file):

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)


    for i, (k, v) in enumerate(pf_dict.items()):

if __name__ == "__main__":
    print("running")