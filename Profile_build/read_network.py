# For network reading and longest prefix match (CIDR format)
# Yebo Feng

import SubnetTree

def read():
    f = open('localprefs.frgp','r')
    text = f.readlines()
    f.close()
    networks = []
    for i in text:
        networks.append(i.strip())
    return networks

def build_tree(networks):
    networks_tree = SubnetTree.SubnetTree()
    for i in networks:
        networks_tree[i] = "protected_network"
    return networks_tree

def read_build_tree():
    return build_tree(read())

if __name__ == "__main__":
    # test whether the prefixes are read correctly
    t = build_tree(read())
    # test cases
    print(b'192.0.2.10' in t) # False
    print(b'142.48.190.1' in t) # True
    print(b'192.0.2.9' in t) # False
    print(b'14.181.124.2' in t) # True
    print(b'192.0.3.9' in t) # False
    print(b'15.73.88.3' in t) # True
    print(b'1.0.0.2' in t) # False
    print(b'11.58.216.5' in t) # True