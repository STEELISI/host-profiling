
import re

def read_files(f1,f2):
    results = dict()
    with open(f1) as fp: 
        Lines = fp.readlines() 
        for line in Lines: 
            if "any" in line and "-" in line:
                line = line.strip()
                ip = re.findall(r"(\d+\.\d+\.\d+\.\d+)",line)[0]
                flow = int(re.findall(r".+ (\d+)\(.+\(.+\(",line)[0])
                packet = int(re.findall(r".+ (\d+)\(.+\(",line)[0])
                byte = int(re.findall(r".+ (\d+)\(",line)[0])
                pps = int(re.findall(r".+\).+\).+\)\ +(\d+)",line)[0])
                bps = int(re.findall(r".+\).+\).+\)\ +\d+\ +(\d+)",line)[0])
                bpp = int(re.findall(r".+\).+\).+\)\ +\d+\ +\d+\ +(\d+)",line)[0])
                if ip in results:
                    temp = results[ip]
                    temp[0] += 1
                    temp[1] += flow
                    temp[2] += packet
                    temp[3] += byte
                    results[ip] = temp
                else:
                    temp = [1,flow,packet,byte,pps,bps,bpp]
                    results[ip] = temp
    with open(f2) as fp: 
        Lines = fp.readlines() 
        for line in Lines: 
            if "any" in line and "-" in line:
                line = line.strip()
                ip = re.findall(r"(\d+\.\d+\.\d+\.\d+)",line)[0]
                flow = int(re.findall(r".+ (\d+)\(.+\(.+\(",line)[0])
                packet = int(re.findall(r".+ (\d+)\(.+\(",line)[0])
                byte = int(re.findall(r".+ (\d+)\(",line)[0])
                pps = int(re.findall(r".+\).+\).+\)\ +(\d+)",line)[0])
                bps = int(re.findall(r".+\).+\).+\)\ +\d+\ +(\d+)",line)[0])
                bpp = int(re.findall(r".+\).+\).+\)\ +\d+\ +\d+\ +(\d+)",line)[0])
                if ip in results:
                    temp = results[ip]
                    temp[0] += 1
                    temp[1] += flow
                    temp[2] += packet
                    temp[3] += byte
                    results[ip] = temp
                else:
                    temp = [1,flow,packet,byte,pps,bps,bpp]
                    results[ip] = temp
    return results


if __name__ == "__main__":
    ip_list = read_files("data/top_bytes_2020_04.csv","data/top_bytes_2020_03.csv")
    a = {k: v for k, v in sorted(ip_list.items(), key=lambda item: item[1])}
    for key in a.keys():
        print(key,a[key])