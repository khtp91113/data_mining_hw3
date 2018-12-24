def read_file(path):
    f = open(path, 'r')
    directed_f = open('hw3dataset/directed.txt', 'w')
    bidirected_f = open('hw3dataset/bidirected.txt', 'w')
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        vertexs = line.split()
        start = int(vertexs[1])
        end = int(vertexs[2])
        directed_f.write(str(start)+','+str(end))
        directed_f.write('\n')
        bidirected_f.write(str(start)+','+str(end))
        bidirected_f.write('\n')
        bidirected_f.write(str(end)+','+str(start))
        bidirected_f.write('\n')
    f.close()
    directed_f.close()
    bidirected_f.close()
    return

def main():
    read_file(path='hw3dataset/origin.txt')
    
if __name__ == '__main__':
    main()