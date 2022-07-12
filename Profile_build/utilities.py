
def read_command(filename):
    command = list()
    with open(filename, 'r') as file:
        text = file.read().strip()
        command = text.split("\n")
    return command

if __name__ == "__main__":
    # for test
    print(read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single_defined.txt"))