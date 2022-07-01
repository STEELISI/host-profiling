# Author: Yebo Feng

import os
import time
import subprocess
import ports_for_analysis as pa

def get_files(path):
    # path = '/data/2019'
    files = []
    ## r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if 'nfcapd.' in file:
                files.append(os.path.join(r, file))
    # for f in files:
    #     print(f)

    return files

def write_to_csv(file,items):
    str = ','
    text = str.join(items)
    with open(file, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text)


def run_bash(command,opt):
    if opt == 1:
        commands = command.split(' ')
        result = subprocess.run(commands, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()
    if opt == 2:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        return output.decode('utf-8').strip()

def get_general_info(file):
    ## id,first,msec_first,Last,msec_last,Flows,Flows_tcp,Flows_udp,Flows_icmp,Flows_other,Packets,Packets_tcp,Packets_udp,Packets_icmp,Packets_other,Bytes,Bytes_tcp,Bytes_udp,Bytes_icmp,Bytes_other
    general_info = []
    general_info.append(file.split('nfcapd.')[1])
    command = "nfdump -r" + file + " -I -N"
    result = run_bash(command,1)
    results = result.split('\n')

    ## timestamps
    general_info.append(results[16].split(' ')[1])
    general_info.append(results[18].split(' ')[1])
    general_info.append(results[17].split(' ')[1])
    general_info.append(results[19].split(' ')[1])

    ## number of flows
    general_info.append(results[1].split(' ')[1])
    general_info.append(results[2].split(' ')[1])
    general_info.append(results[3].split(' ')[1])
    general_info.append(results[4].split(' ')[1])
    general_info.append(results[5].split(' ')[1])
    
    ## number of packets
    general_info.append(results[6].split(' ')[1])
    general_info.append(results[7].split(' ')[1])
    general_info.append(results[8].split(' ')[1])
    general_info.append(results[9].split(' ')[1])
    general_info.append(results[10].split(' ')[1])

    ## number of bytes
    general_info.append(results[11].split(' ')[1])
    general_info.append(results[12].split(' ')[1])
    general_info.append(results[13].split(' ')[1])
    general_info.append(results[14].split(' ')[1])
    general_info.append(results[15].split(' ')[1])

    return general_info

def get_ports_info(file,ports):
    ## total_flows,total_bytes,total_packets,avg_bps,avg_pps,avg_bpp
    command = "nfdump -r " +  file
    subcommand = []
    for i in ports:
        subcommand.append("(port "+str(i)+")")
    filter_command = ' or '.join(subcommand)
    command = command +' \''+filter_command+'\''+ ' -s Proto -N'
    # print(command)
    
    result = run_bash(command,2)
    results = result.split('\n')

    ports_info = []
    for i in results[len(results)-4].split(', '):
        temp = i.split(': ')
        ports_info.append(temp[len(temp)-1])
    return ports_info

def test():
    files = get_files('/data/2019')
    write_to_csv('a.txt',['1','2','3'])
    print(pa.ports)
    print(get_general_info("/data/2020/04/06/nfcapd.202004060505"))
    print(get_ports_info("/data/2020/04/06/nfcapd.202004060505",[123,23,80]))

if __name__=="__main__":
    files = get_files('/Users/yebof/Documents/data')
    for f in files:
        record = get_general_info(f)
        for p in pa.ports:
            record = record + get_ports_info(f,p)
        write_to_csv('data2020.csv',record)
        print(record[0]+" Completed!")
