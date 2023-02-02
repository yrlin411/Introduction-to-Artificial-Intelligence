import csv
from collections import defaultdict
from dis import dis
from turtle import distance
edgeFile = 'edges.csv'


class n:
    def __init__(self, End, distance, limit):  # define a class to store the data of an edge
        self.End = End  # including the end, the distance, and the speed limit
        self.distance = distance
        self.limit = limit


def ucs(start, end):
    # Begin your code (Part 3)

    # read data
    EdgeFile = open('edges.csv')  # open 'edges.csv'
    lines = EdgeFile.readlines()  # read them as separate lines
    # create a dictionary to store the edges from the same start
    graph = defaultdict(list)
    # create a dictionary to see which has been visited
    visited = defaultdict(str)

    for line in lines:
        data = line.split(",")  # store the data from csv file
        Node = n(data[1], data[2], data[3].replace("\n", ""))
        graph[data[0]].append(Node)
        graph[data[0]].sort(key=lambda Node: Node.End)
        visited[data[0]] = False  # set all elements to not visited

    # ucs
    q = []  # create a list for ucs
    q.append(start)  # push the start node inside
    visited[str(start)] = True  # mark the start as visited
    # create a dictionary to store the distance from 'start'
    distance = defaultdict(float)
    distance[start] = 0  # the distace from 'start' to 'start' is 0
    parent = defaultdict(str)  # create a dictionary to store the previous node
    parent[start] = None  # start with no previous node
    num_visited = 0

    while len(q) != 0:  # while the queue is not empty
        min = float("inf")  # set the minimum to infinity
        for i in range(len(q)):  # for the distances to the ends in current queue
            if distance[q[i]] < min:  # if it is smaller than the minimum
                min = distance[q[i]]  # update the minimum
                m_index = i  # record the index
        # set current node to the one with minimum distance
        current = str(q.pop(m_index))
        visited[current] = True  # mark as visited
        num_visited += 1  # so the number of visited nodes increases
        if current == str(end):  # if the node is 'end'
            del q[:]  # break the loop
            # set the total distance to the distance to 'end'
            dist = distance[str(end)]
            break
        # for every edge starting from current node
        for i in range(len(graph[current])):
            # set the end of this edge to the next node
            next = graph[current][i].End
            if visited[next] == False:  # if the next is not visited
                if next not in q:  # and if it is not in the queue yet
                    q.append(next)  # add it to the queue
                if next in distance:  # if it already has a distance
                    if distance[next] > distance[current] + float(graph[current][i].distance):
                        # and if there exists smaller distance, update
                        parent[next] = current
                        distance[next] = distance[current] + \
                            float(graph[current][i].distance)
                else:  # if next does not have a recorded distance yet
                    parent[next] = current  # do the same as above
                    distance[next] = distance[current] + \
                        float(graph[current][i].distance)
        # set the used distance back to infinity
        distance[m_index] = float("inf")

    path = []  # create a queue for storing the path
    path.append(str(end))  # push the end node inside
    turn = 0  # the first iteration
    while path[turn] != str(start):  # while the current node is not 'start'
        path.append(parent[path[turn]])  # add the previous node to the path
        turn += 1  # next iteration

    path.reverse()  # reverse because it was stored bakwards
    for i in range(len(path)):  # change all the elements in the path to integers
        path[i] = int(path[i])

    return path, dist, num_visited  # return

    raise NotImplementedError("To be implemented")
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
