import os
import utilities as ut

def print_n_profiles_v2(file,num):
    # print the first n elements in the profile dictionary

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    it = iter(pf_dict)

    for i in range(num):
        dict_key = next(it)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(dict_key) + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("========== " + "Traffic" " ==================================================================")
        for i, (k, v) in enumerate(pf_dict[dict_key][0].items()):
            print(k + ": " + str(v))
        print("========== " + "restricted or unrestricted" " ===============================================")
        for i, (k, v) in enumerate(pf_dict[dict_key][1].items()):
            print(k + ": " + str(v[0]))
        print("========== " + "End" " ======================================================================")
        print()
        print()

if __name__ == "__main__":
    print("running")