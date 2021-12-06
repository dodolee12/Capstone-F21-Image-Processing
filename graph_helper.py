import math
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import numpy as np

FILTER_DISTANCE = 50

def image_to_points(img):
    # convert to graph
    indices = np.where(img < [240])

    # for some reason this allows to to be right side up.
    x_coords = indices[1]
    y_coords = -indices[0]

    num_total_points = len(x_coords)
    filter = 2
    pixel_coords = []
    plot_x = []
    plot_y = []

    # Getting points into list
    for i in range(num_total_points):
        # cutting number of points by filter
        if i % filter == 0:
            pixel_coords.append((x_coords[i], y_coords[i]))
            plot_x.append(x_coords[i])
            plot_y.append(y_coords[i])

    #pixel_coords.sort()

    return pixel_coords,plot_x,plot_y

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def create_graph(list_of_points, size):
    coordinate_point_graph = []

    for i in range(size):
        ith_coord_edges = []

        for j in range(size):
            point_distance = distance(list_of_points[i], list_of_points[j])
            #Set threshold for gaps in signature
            if point_distance < FILTER_DISTANCE:
                ith_coord_edges.append(point_distance)
            else:
                ith_coord_edges.append(0)

        coordinate_point_graph.append(ith_coord_edges)

    return coordinate_point_graph

def minimum_spanning_graph(graph):
    all_graph_edges = csr_matrix(graph)
    connected_lines = minimum_spanning_tree(all_graph_edges).toarray().astype(float)
    return connected_lines

def reflect_over_diagonal(graph, size):
    #reflect over [i][j]
    for i in range(size):
        for j in reversed(range(size)):
            if graph[i][j]:
                graph[j][i] = graph[i][j]

    return graph

def adjacency_matrix_to_adjacency_list(graph, size):
    graph_adjacency_lists = []

    for i in range(size):
        point_adjacency_list = []
        for j in range(size):
            if graph[i][j]:
                point_adjacency_list.append(j)
        graph_adjacency_lists.append(point_adjacency_list)

    return graph_adjacency_lists