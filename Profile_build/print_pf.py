from itertools import islice
import utilities as ut
import os
import argparse

def print_nth_profile(file,num):
    # print the nth element in the profile dictionary
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    it = iter(pf_dict)
    # Consume n elements.
    next(islice(it, num, num), None) 
    # Return the value at the current position.
    # This raises StopIteration if n is beyond the limits.
    # Use next(it, None) to suppress that exception.
    item = next(it)

    print(item)
    print(pf_dict[item])

def print_n_profiles(file,num):
    # print the first n elements in the profile dictionary

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    it = iter(pf_dict)

    for i in range(num):
        dict_key = next(it)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(dict_key) + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("========== " + "Outbound Traffic" " =========================================================")
        for i, (k, v) in enumerate(pf_dict[dict_key][0].items()):
            print(k + ": " + str(v))
        print("========== " + "Inbound Traffic" " ================================================")
        for i, (k, v) in enumerate(pf_dict[dict_key][1].items()):
            print(k + ": " + str(v))
        print("========== " + "End" " ======================================================================")
        print()
        print()

def print_n_simplified_profiles(file,num):
    # print the first n elements in the simplified profile dictionary
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    it = iter(pf_dict)

    for i in range(num):
        dict_key = next(it)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(dict_key) + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("Topic of this IP: ")
        print(pf_dict[dict_key][0])
        print("========== " + "Traffic volume" " ===========================================================")
        print("Outbound total pkts: " + str(pf_dict[dict_key][1][0]))
        print("Outbound total bytes: " + str(pf_dict[dict_key][1][1]))
        print("Inbound total pkts: " + str(pf_dict[dict_key][1][2]))
        print("Inbound total bytes: " + str(pf_dict[dict_key][1][3]))
        print("========== " + "Detailed port information" " ================================================")
        for i, (k, v) in enumerate(pf_dict[dict_key][2].items()):
            print(k + ": " + str(v))
        print("========== " + "End" " ======================================================================")
        print()
        print()

if __name__ == "__main__":
    # Examples:
    #     python3 print_pf.py -spf "results/8.17_simplified_profile_results.txt" -n 20
    #     python3 print_pf.py -pf "results/8.17_profile_results.txt" -n 20


    parser = argparse.ArgumentParser()
    parser.add_argument('-spf', type=str, help='The path of the simplified profile you want to print. For example: \"results/8.17_simplified_profile_results.txt\".')
    parser.add_argument('-pf', type=str, help='The path of the profile you want to print. For example: \"results/8.17_profile_results.txt\".')
    parser.add_argument('-n', type=int, help='The number of items you want to print. For example: 20.')
    args = parser.parse_args()

    if args.pf:
        print_n_profiles(args.pf, args.n)
    elif args.spf:
        print_n_simplified_profiles(args.spf, args.n)
