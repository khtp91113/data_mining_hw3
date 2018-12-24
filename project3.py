import time
child = {}
parent = {}
# set node nums for each graph
node_nums = [6, 5, 4, 7, 469, 1228, 9823, 9823]
s = []

def read_file(path):
    global child, parent
    child = {}
    parent = {}
    f = open(path, 'r')
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        # read vertex
        vertexs = line.split(',')
        start = int(vertexs[0])
        end = int(vertexs[1])
        # save relationship
        if start in child:
            child[start].append(end)
        else:
            child[start] = [end]
        if end in parent:
            parent[end].append(start)
        else:
            parent[end] = [start]
    f.close()
    return
    
# calculate authority and hubs
def cal(mode, node, arr):
    if mode == 'parent':
        if node not in parent:
            return 0
        sum = 0
        for x in parent[node]:
            sum += arr[x-1]
        return sum
    else:
        if node not in child:
            return 0
        sum = 0
        for x in child[node]:
            sum += arr[x-1]
        return sum

# calculate different between old and new values
def diff(new, old):
    sum = 0
    for i in range(0, len(new)):
        sum += abs(new[i]-old[i])
    return sum

# do hits algorithm    
def hits(node_num):
    a = [1.0 for x in range(0, node_num)]
    h = [1.0 for x in range(0, node_num)]
    threshold = 0.1
    nodes = [x for x in range(1, node_num+1)]
    while True:
        new_a = []
        new_h = []
        for node in nodes:
            new_a.append(cal('parent', node, h))
            new_h.append(cal('child', node, a))
        new_a_sum = sum(new_a)
        new_a = [x/new_a_sum for x in new_a]
        new_h_sum = sum(new_h)
        new_h = [x/new_h_sum for x in new_h]
        # if converge, stop
        if diff(new_a, a)+diff(new_h, h) < threshold:
            a = new_a
            h = new_h
            break
        a = new_a
        h = new_h
    return a, h
    
# calculate pagerank
def pagerank(node_num):
    # average value
    x = [1.0/node_num for i in range(0, node_num)]
    threshold = 0.1
    d = 0.15
    while True:
        new_x = []
        for i in range(0, node_num):
            if i+1 not in parent:
                new_x.append(d/node_num)
            else:
                sums = 0
                for pa in parent[i+1]:
                    sums += x[pa-1]/len(child[pa])
                new_x.append(d/node_num + (1-d)*sums)
        # if converge, stop
        if diff(list(new_x), list(x)) < threshold:
            x = new_x
            break
        x = new_x
    return x

# calculate sim_rank of node1 and node2
def calc_s(node1, node2):
    global s
    # same node
    if node1 == node2:
        return 1
    # end point
    if node1 not in parent or node2 not in parent:
        return 0
    C = 0.5
    len1 = len(parent[node1])
    len2 = len(parent[node2])
    sums = 0
    for i in range(0, len1):
        for j in range(0, len2):
            sums += s[parent[node1][i]-1][parent[node2][j]-1]
    sums = C*sums/(len1*len2)
    return sums
    
# iterative calculate sim_rank(depth=1) until converge 
def sim_rank(node_num):
    global s
    s = []
    # initial sim_rank values
    for i in range(0, node_num):
        s.append([0 for j in range(0, node_num)])
        s[i][i] = 1.0
    times = 10000
    # iterative calculate sim_rank
    for iterative in range(0, times):
        new_s = []
        for i in range(0, node_num):
            new_s.append([0 for j in range(0, node_num)])
        for i in range(0, node_num):
            for j in range(i, node_num):
                new_s[i][j] = calc_s(i+1, j+1)
                new_s[j][i] = new_s[i][j]
        # if converge, stop
        if cmp(new_s, s) == 0:
            s = new_s
            break
        s = new_s
    return s

# add new edges for node 0 to other nodes
def add_edge(node_num, file):
    file.write('Add edges: \n')
    if 1 not in child:
        child[1] = []
    if 1 not in parent:
        parent[1] = []
    for i in range(2, node_num+1):
        if i not in child:
            child[i] = []
        if i not in parent:
            parent[i] = []
        child[i].append(1)
        parent[1].append(i)
        parent[i].append(1)
        child[1].append(i)
        file.write('(1,' + str(i) + ')')
        file.write('(' + str(i) + ',1)')
    file.write('\n')
    
def main():
    # output result to 3 files
    f_part1 = open('part1.txt', 'w')
    f_part2 = open('part2.txt', 'w')
    f_part3 = open('part3.txt', 'w')
    for i in range(1, 9):
        path = 'hw3dataset/'
        if i == 7:
            path += 'directed.txt'
        elif i == 8:
            path += 'bidirected.txt'
        else:
            path += 'graph_' + str(i) + '.txt'
        read_file(path)
        start = time.time()
        a, h = hits(node_nums[i-1])
        hits_done = time.time()
        pr = pagerank(node_nums[i-1])
        end = time.time()
        f_part1.write('graph' + str(i) + '\n')
        f_part1.write('authority= ')
        f_part1.write(str(a) + '\n')
        f_part1.write('hubs= ')
        f_part1.write(str(h) + '\n')
        f_part1.write('pagerank= ')
        f_part1.write(str(pr) + '\n')
        time1 = round(hits_done-start, 4)
        time2 = round(end-hits_done, 4)
        f_part1.write('Time(sec): Hits=' + str(time1) + ', Pagerank=' + str(time2) + '\n\n')
    for i in range(1, 6):
        path = 'hw3dataset/graph_' + str(i) + '.txt'
        read_file(path)
        start = time.time()
        s = sim_rank(node_nums[i-1])
        end = time.time()
        f_part2.write('graph' + str(i) + '\n')
        f_part2.write('sim_rank= ')
        f_part2.write(str(s) + '\n')
        time1 = round(end-start, 4)
        f_part2.write('Time(sec): Simrank=' + str(time1) + '\n\n')
    for i in range(1, 4):
        path = 'hw3dataset/graph_' + str(i) + '.txt'
        read_file(path)
        f_part3.write('graph ' + str(i) + '\n')
        a, h = hits(node_nums[i-1])
        pr = pagerank(node_nums[i-1])     
        add_edge(node_nums[i-1], f_part3)
        f_part3.write('origin: authority=' + str(round(a[0], 3)) + ', hub=' + str(round(h[0], 3)) + ', pagerank=' + str(round(pr[0], 3)) + '\n')
        a, h = hits(node_nums[i-1])
        pr = pagerank(node_nums[i-1])
        f_part3.write('After: authority=' + str(round(a[0], 3)) + ', hub=' + str(round(h[0], 3)) + ', pagerank=' + str(round(pr[0], 3)) + '\n\n')
    f_part1.close()
    f_part2.close()
    f_part3.close()
    
if __name__ == '__main__':
    main()