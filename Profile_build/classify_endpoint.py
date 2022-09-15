# Yebo Feng 

from email.headerregistry import Address
import os
import utilities as ut

def is_restricted(ip):
    # return 0 if this ip is not restricted
    # return 1 if this ip is restricted

    global profile_v2_dict

    return 0

def has_bidirectional_traffic(ip):
    # return 0 if does not have bidirectional traffic
    # return 1 if has bidirectional traffic

    global profile_v1_dict

    return 0

def separate_ip(profile_v1_file, profile_v2_file, simplified_profile_file):

    global profile_v1_dict
    global profile_v2_dict
    global simplified_profile_dict

    # load all types of profiles 
    print("Loading all the profiles......")
    dirname = os.path.dirname(__file__)
    profile_v1_filename = os.path.join(dirname, profile_v1_file)
    profile_v1_dict = ut.dict_read_from_file(profile_v1_filename)
    profile_v2_filename = os.path.join(dirname, profile_v2_file)
    profile_v2_dict = ut.dict_read_from_file(profile_v2_filename)
    simplified_profile_filename = os.path.join(dirname, simplified_profile_file)
    simplified_profile_dict = ut.dict_read_from_file(simplified_profile_filename)

    # extract all the IP addresses as a list 

if __name__ == "__main__":
    print("running")