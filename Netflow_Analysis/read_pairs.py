# Yebo Feng


import os

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

def read_pair(filename):

    total_flow = 0
    total_bytes = 0
    ntp_flow = 0
    ntp_bytes = 0
    dns_flow = 0
    dns_bytes = 0
    https_flow = 0
    https_bytes = 0
    http_flow = 0
    http_bytes = 0
    smtp_flow = 0
    smtp_bytes = 0
    pop_flow = 0
    pop_bytes = 0
    ssh_flow = 0
    ssh_bytes = 0
    telnet_flow = 0
    telnet_bytes = 0
    ftp_flow = 0
    ftp_bytes = 0
    vpn_flow = 0
    vpn_bytes = 0

    bj_flow = 0
    bj_bytes = 0
    gmeet_flow = 0
    gmeet_bytes = 0
    goto_flow = 0
    goto_bytes = 0
    highhigh_flow = 0
    highhigh_bytes = 0
    icmp_flow = 0
    icmp_bytes = 0
    noservice_flow = 0
    noservice_bytes = 0
    oddprot_flow = 0
    oddprot_bytes = 0
    skype_flow = 0
    skype_bytes = 0
    syn_flow = 0
    syn_bytes = 0
    twoservice_flow = 0
    twoservice_bytes = 0
    valve_flow = 0
    valve_bytes = 0
    webex_flow = 0
    webex_bytes = 0
    zoom_flow = 0
    zoom_bytes = 0

    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in lines[1:]:
            if "fid" in i:
                continue
            else:
                if i[0].isdigit():
                    if i.startswith("123 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        ntp_flow = int(infos[0].strip())
                        ntp_bytes = float(infos[1].strip())
                        total_flow += ntp_flow
                        total_bytes += ntp_bytes
                    elif i.startswith("53 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        dns_flow = int(infos[0].strip())
                        dns_bytes = float(infos[1].strip())
                        total_flow += dns_flow
                        total_bytes += dns_bytes
                    elif i.startswith("443 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        https_flow = int(infos[0].strip())
                        https_bytes = float(infos[1].strip())
                        total_flow += https_flow
                        total_bytes += https_bytes
                    elif i.startswith("80 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        http_flow = int(infos[0].strip())
                        http_bytes = float(infos[1].strip())
                        total_flow += http_flow
                        total_bytes += http_bytes
                    elif i.startswith("25 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        smtp_flow = int(infos[0].strip())
                        smtp_bytes = float(infos[1].strip())
                        total_flow += smtp_flow
                        total_bytes += smtp_bytes
                    elif i.startswith("110 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        pop_flow = int(infos[0].strip())
                        pop_bytes = float(infos[1].strip())
                        total_flow += pop_flow
                        total_bytes += pop_bytes
                    elif i.startswith("22 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        ssh_flow = int(infos[0].strip())
                        ssh_bytes = float(infos[1].strip())
                        total_flow += ssh_flow
                        total_bytes += ssh_bytes
                    elif i.startswith("23 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        telnet_flow = int(infos[0].strip())
                        telnet_bytes = float(infos[1].strip())
                        total_flow += telnet_flow
                        total_bytes += telnet_bytes
                    elif i.startswith("20 flows") or i.startswith("21 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        ftp_flow += int(infos[0].strip())
                        ftp_bytes += float(infos[1].strip())
                        total_flow += int(infos[0].strip())
                        total_bytes += float(infos[1].strip())
                    elif i.startswith("4500 flows") or i.startswith("4501 flows") or i.startswith("4502 flows"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        vpn_flow += int(infos[0].strip())
                        vpn_bytes += float(infos[1].strip())
                        total_flow += int(infos[0].strip())
                        total_bytes += float(infos[1].strip())
                    else:
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        total_flow += int(infos[0].strip())
                        total_bytes += float(infos[1].strip())
                else:
                    if i.startswith("bj"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        bj_flow = int(infos[0].strip())
                        bj_bytes = float(infos[1].strip())
                    elif i.startswith("gmeet"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        gmeet_flow = int(infos[0].strip())
                        gmeet_bytes = float(infos[1].strip())
                    elif i.startswith("goto"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        goto_flow = int(infos[0].strip())
                        goto_bytes = float(infos[1].strip())
                    elif i.startswith("highhigh"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        highhigh_flow = int(infos[0].strip())
                        highhigh_bytes = float(infos[1].strip())
                    elif i.startswith("icmp"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        icmp_flow = int(infos[0].strip())
                        icmp_bytes = float(infos[1].strip())
                    elif i.startswith("noservice"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        noservice_flow = int(infos[0].strip())
                        noservice_bytes = float(infos[1].strip())
                    elif i.startswith("oddprot"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        oddprot_flow = int(infos[0].strip())
                        oddprot_bytes = float(infos[1].strip())
                    elif i.startswith("skype"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        skype_flow = int(infos[0].strip())
                        skype_bytes = float(infos[1].strip())
                    elif i.startswith("syn"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        syn_flow = int(infos[0].strip())
                        syn_bytes = float(infos[1].strip())
                    elif i.startswith("twoservice"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        twoservice_flow = int(infos[0].strip())
                        twoservice_bytes = float(infos[1].strip())
                    elif i.startswith("valve"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        valve_flow = int(infos[0].strip())
                        valve_bytes = float(infos[1].strip())
                    elif i.startswith("webex"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        webex_flow = int(infos[0].strip())
                        webex_bytes = float(infos[1].strip())
                    elif i.startswith("zoom"):
                        info = i.split('flows')[1]
                        infos = info.split('bytes')
                        zoom_flow = int(infos[0].strip())
                        zoom_bytes = float(infos[1].strip())
    f_name = filename.split('nfcapd.')[1].strip()
    dataset = [f_name, total_flow, total_bytes, ntp_flow, ntp_bytes, dns_flow, dns_bytes, https_flow, https_bytes, http_flow, 
               http_bytes, smtp_flow, smtp_bytes, pop_flow, pop_bytes, ssh_flow, ssh_bytes, telnet_flow, telnet_bytes, 
               ftp_flow, ftp_bytes, vpn_flow, vpn_bytes, bj_flow, bj_bytes, gmeet_flow, gmeet_bytes, goto_flow, goto_bytes, 
               highhigh_flow, highhigh_bytes, icmp_flow, icmp_bytes, noservice_flow, noservice_bytes, oddprot_flow, oddprot_bytes, 
               skype_flow, skype_bytes, syn_flow, syn_bytes, twoservice_flow, twoservice_bytes, valve_flow, valve_bytes, 
               webex_flow, webex_bytes, zoom_flow, zoom_bytes]
    return dataset

def write_to_csv(file,items):
    items_str = []
    for i in items:
        items_str.append(str(i))
    str_m = ','
    text = str_m.join(items_str)
    with open(file, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text)

def test():
    f = "/Users/fengyebo/Desktop/COVID-19_traffic_analysis/nfcapd.202004231455"
    f2 = "/Users/fengyebo/Desktop/COVID-19_traffic_analysis/pair.txt"
    records = read_pair(f)
    write_to_csv(f2,records)

if __name__ == "__main__":
    files = get_files('/scratch/UO/pairs_data/')
    for f in files:
        record = read_pair(f)
        write_to_csv('pairs_data.csv',record)
        print(record[0]+" Completed!")