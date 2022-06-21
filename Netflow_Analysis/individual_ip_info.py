# Author: Yebo Feng

import os
import time
import subprocess
import ips
import client_ips

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

def get_general_info(file,ip):
    ## id,flows,packets,bytes
    general_info = []
    general_info.append(file.split('nfcapd.')[1])

    command = "nfdump -r " + file + " 'ip " + ip + "' -o \"fmt:%ra,%fl,%pkt,%byt\" -N"
    # print(command)
    result = run_bash(command,2)
    results = result.split('\n')

    if len(results) == 6:
        general_info = general_info + ["0","0","0"]
        return general_info
    else:
        flows = 0
        packets = 0
        byte = 0
        records = results[1:len(results)-5]
        for i in records:
            items = i.split(',')
            if "141" in items[0] or "140" in items[0].strip():
                flows = flows + int(items[1].strip())
                packets = packets + int(items[2].strip()) * 100 /4096
                byte = byte + int(items[3].strip()) * 100 /4096
            else:
                flows = flows + int(items[1].strip())
                packets = packets + int(items[2].strip())
                byte = byte + int(items[3].strip())
        # print(records)
        # print(avg_info)
        general_info = general_info + [str(flows),str(packets),str(byte)]
        return general_info

def get_ip_info(file,ip):
    ## id,total_flows,total_bytes,total_packets,avg_bps,avg_pps,avg_bpp
    command = "nfdump -r " + file + " 'ip " + ip + "' -s record -N"
    
    result = run_bash(command,2)
    results = result.split('\n')

    ip_info = []
    ip_info.append(file.split('nfcapd.')[1])
    for i in results[len(results)-4].split(', '):
        temp = i.split(': ')
        ip_info.append(temp[len(temp)-1])
    return ip_info

def test():
    ip = "7.29.11.61"
    # ip = '1.1.1.1'
    print(get_general_info("/data/2020/04/05/nfcapd.202004050515",ip))

if __name__=="__main__":

    file0 = get_files('/data/2020/02')
    file1 = get_files('/data/2020/03')
    file2 = get_files('/data/2020/04')
    files = file0 + file1 + file2
    for f in files:
        for ip in client_ips.ips:
            record = get_general_info(f,ip)
            write_to_csv("client_ip_data/"+ip,record)
        print(f.split('nfcapd.')[1]+" Completed!")