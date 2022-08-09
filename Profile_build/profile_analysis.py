# Yebo Feng

from locale import normalize
import os
import utilities as ut
import copy
import pandas as pd

def profile_to_matrix_dict(file, ip):

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    target_profile = pf_dict[ip]
    outbound_profile_dict = target_profile[0]
    inbound_profile_dict = target_profile[1]

    outbound_matrix_dict = single_direction_to_matrix(outbound_profile_dict)
    inbound_matrix_dict = single_direction_to_matrix(inbound_profile_dict)

    # outbound_matrix_df = pd.DataFrame.from_dict(outbound_matrix_dict)
    # inbound_matrix_df = pd.DataFrame.from_dict(inbound_matrix_dict)
    # print(outbound_matrix_df)
    # print(inbound_matrix_df)
    # return outbound_matrix_df, inbound_matrix_df

    return outbound_matrix_dict, inbound_matrix_dict

def martixdict_to_matrix(matrix_dict, pkts_or_bytes = 2):
    # pkts_or_bytes = 1 means choose the pkts
    # pkts_or_bytes = 2 means choose the bytes
    service_matrix_index = []
    noservice_matrix_index = []
    for num, (k, v) in enumerate(matrix_dict.items()):
        if "---" in k:
            noservice_matrix_index.append(k)
        else:
            service_matrix_index.append(k)
    
    # sort from large to small 
    def sort_key1(e):
            return int(e)
    service_matrix_index.sort(reverse = False, key = sort_key1)
    def sort_key2(e):
            return int(e.split("---")[0])
    noservice_matrix_index.sort(reverse = False, key = sort_key2)

    service_matrix = []
    noservice_matrix = []
    for i in service_matrix_index:
        new_list = copy.deepcopy(matrix_dict[i])
        list_to_be_add = []
        for item in new_list:
            list_to_be_add.append(item[pkts_or_bytes - 1])
        service_matrix.append(copy.deepcopy(list_to_be_add))
    for j in noservice_matrix_index:
        new_list = copy.deepcopy(matrix_dict[j])
        list_to_be_add = []
        for item in new_list:
            list_to_be_add.append(item[pkts_or_bytes - 1])
        noservice_matrix.append(copy.deepcopy(list_to_be_add))
    
    # print(service_matrix_index)
    # print("="*30)
    # print(service_matrix)
    # print("="*30)
    # print(len(service_matrix))
    # print("="*30)
    # print(noservice_matrix_index)
    # print("="*30)
    # print(noservice_matrix)
    # print("="*30)
    # print(len(noservice_matrix))

    return service_matrix, service_matrix_index, noservice_matrix, noservice_matrix_index

def normalize_matrix(matrix1, matrix2, matrix3, matrix4):
    max_num = 0

    # figure out the max value 
    for items in matrix1:
        # print(items)
        temp_max = max(items)
        if temp_max > max_num:
            max_num = temp_max
    for items in matrix2:
        temp_max = max(items)
        if temp_max > max_num:
            max_num = temp_max
    for items in matrix3:
        temp_max = max(items)
        if temp_max > max_num:
            max_num = temp_max
    for items in matrix4:
        temp_max = max(items)
        if temp_max > max_num:
            max_num = temp_max

    new_matrix1 = copy.deepcopy(matrix1)
    new_matrix2 = copy.deepcopy(matrix2)
    new_matrix3 = copy.deepcopy(matrix3)
    new_matrix4 = copy.deepcopy(matrix4)

    # normalizing 
    for i in range(len(new_matrix1)):
        for j in range(len(new_matrix1[i])):
            new_matrix1[i][j] = new_matrix1[i][j]/max_num
    for i in range(len(new_matrix2)):
        for j in range(len(new_matrix2[i])):
            new_matrix2[i][j] = new_matrix2[i][j]/max_num
    for i in range(len(new_matrix3)):
        for j in range(len(new_matrix3[i])):
            new_matrix3[i][j] = new_matrix3[i][j]/max_num
    for i in range(len(new_matrix4)):
        for j in range(len(new_matrix4[i])):
            new_matrix4[i][j] = new_matrix4[i][j]/max_num

    return new_matrix1, new_matrix2, new_matrix3, new_matrix4


def single_direction_to_matrix(single_direction_dict):

    single_direction_matrix = {}
    for i, (k, v) in enumerate(single_direction_dict.items()):
        index = k.split("|")[1]
        time_range = k.split("|")[0]
        start_time = time_range.split("-")[0]
        start_hour = int(start_time.split(":")[0])
        start_minute = int(start_time.split(":")[1])

        # this sequence starts from 0 
        sequence = int((start_hour * 60 + start_minute)/5)
        if index not in single_direction_matrix:
            # 24 hours cut to 5 min units 
            single_direction_matrix[index] = [[0,0]] * 288
        single_direction_matrix[index][sequence] = [v[0], v[1]]
    
    return single_direction_matrix

def generate_normalized_profile_martix(filename, ip, pkts_or_bytes):
    # pkts_or_bytes = 1 means choose the pkts
    # pkts_or_bytes = 2 means choose the bytes
    outbound_matrix_dict, inbound_matrix_dict = profile_to_matrix_dict(filename, ip)
    out_service_matrix, out_service_matrix_index, out_noservice_matrix, out_noservice_matrix_index = martixdict_to_matrix(outbound_matrix_dict, pkts_or_bytes)
    in_service_matrix, in_service_matrix_index, in_noservice_matrix, in_noservice_matrix_index = martixdict_to_matrix(inbound_matrix_dict, pkts_or_bytes)
    normalized_out_service_matrix, normalized_out_noservice_matrix, normalized_in_service_matrix, normalized_in_noservice_matrix = normalize_matrix(out_service_matrix, out_noservice_matrix, in_service_matrix, in_noservice_matrix)

    # print("out_service_matrix_index"+"="*30)
    # print(out_service_matrix_index)
    # print("normalized_out_service_matrix"+"="*30)
    # print(normalized_out_service_matrix)
    # print(len(normalized_out_service_matrix))
    # print("out_noservice_matrix_index"+"="*30)
    # print(out_noservice_matrix_index)
    # print("out_noservice_matrix"+"="*30)
    # print(normalized_out_noservice_matrix)
    # print(len(normalized_out_noservice_matrix))
    # print()
    # print()
    # print("in_service_matrix_index"+"="*30)
    # print(in_service_matrix_index)
    # print("normalized_in_service_matrix"+"="*30)
    # print(normalized_in_service_matrix)
    # print(len(normalized_in_service_matrix))
    # print("in_noservice_matrix_index"+"="*30)
    # print(in_noservice_matrix_index)
    # print("in_noservice_matrix"+"="*30)
    # print(normalized_in_noservice_matrix)
    # print(len(normalized_in_noservice_matrix))

    # 8 values 
    return out_service_matrix_index, normalized_out_service_matrix, out_noservice_matrix_index, normalized_out_noservice_matrix, in_service_matrix_index, normalized_in_service_matrix, in_noservice_matrix_index, normalized_in_noservice_matrix


if __name__ == "__main__":
    print("Analyzing ......")
    # profile_to_matrix_dict("results/8.17_profile_results.txt", "68.158.58.84") # complicated server
    # profile_to_matrix_dict("results/8.17_profile_results.txt", "65.89.253.157") # complicated client
    generate_normalized_profile_martix("results/8.17_profile_results.txt", "65.89.253.157", 2)