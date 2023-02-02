import csv
from collections import defaultdict
edgeFile = 'edges.csv'


class n:
    def __init__(self, End, distance, limit):  # define a class to store the data of an edge
        self.End = End  # including the end, the distance, and the speed limit
        self.distance = distance
        self.limit = limit


def dfs(start, end):
    # Begin your code (Part 2)

    # read the data
    EdgeFile = open(edgeFile)  # open 'edges.csv'
    lines = EdgeFile.readlines()  # read them as separate lines
    # create a dictionary to store the edges from the same start
    graph = defaultdict(list)
    # create a dictionary to see which has been visited
    visited = defaultdict(str)

    for line in lines:
        data = line.split(",")  # store the data from csv file
        Node = n(data[1], data[2], data[3].replace("\n", ""))
        graph[data[0]].append(Node)
        visited[data[0]] = False  # set all elements to not visited
    # dfs
    q = []  # create a queue for dfs
    q.append(start)  # push the start node inside
    visited[str(start)] = True  # mark the start as visited
    parent = defaultdict(str)  # create a dictionary to store the previous node
    parent[str(start)] = None  # start with no previous node
    num_visited = 0

    while len(q) != 0:  # while the queue is not empty
        # set the current node to the last element of the queue (FILO)
        current = str(q.pop())
        # for every edge starting from the current node
        for i in range(len(graph[current])):
            next = graph[current][i].End  # set the next node
            if visited[next] == False:  # if the next node is not visited
                # set the previous of the next to current
                parent[next] = current
                visited[str(next)] = True  # visited
                num_visited += 1  # so the number of visited nodes increases
                q.append(next)  # push the next node into the queue
                if next == str(end):  # if this edge reaches the end
                    del q[:]  # break the loop
                    break

    path = []  # create a queue for storing the path
    path.append(str(end))  # push the end node inside
    dist = 0  # initialize the distance to 0
    # now = end  # set the current node to 'end'
    turn = 0  # the first iteration
    while parent[path[turn]] != None:  # while the current node is not 'start'
        # print(parent[path[turn]])
        # for edges starting from the previous node
        for i in range(len(graph[parent[path[turn]]])):
            if graph[parent[path[turn]]][i].End == path[turn]:  # if the End is the current node
                # add up the distance
                dist += float(graph[parent[path[turn]]][i].distance)
        turn += 1  # next iteration
        path.append(parent[path[turn-1]])  # add the previous node to the path
        # now = parent[now]  # set the current node to the previous

    path.reverse()  # reverse because it was stored bakwards
    for i in range(len(path)):  # change all the elements in the path to integers
        path[i] = int(path[i])

    return path, dist, num_visited  # return

    raise NotImplementedError("To be implemented")
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
