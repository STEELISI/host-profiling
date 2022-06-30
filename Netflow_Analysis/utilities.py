# Author: Yebo Feng

from csv import reader
import client_ips

def write_txt(file_path,l):
    with open(file_path,'wt') as f:
        count = 0
        for i in l:
            print(str(count)+","+str(i[1]), file=f)
            count+=1

def read_single_attr(filename,time_start,time_end,index):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            else:
                time_id=int(row[0])
                if time_id>=time_start and time_id<=time_end:
                    temp = []
                    temp.append(time_id)
                    temp.append(float(row[index]))
                    dataset.append(temp)
    return dataset

def time_sort(l):
    def sort_key(e):
        return e[0]
    l.sort(key=sort_key)
    return l

if __name__ == "__main__": 
    # print('test')
    # print(time_sort(read_single_attr('data2020.csv',202002260000,202002262355,20)))

    l = []
    for i in client_ips.ips:
        if not i in l:
            l.append(i)
    print(len(l))
    print(len(client_ips.ips))