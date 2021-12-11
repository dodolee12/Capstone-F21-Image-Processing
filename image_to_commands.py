import cv2
import ftlib as ft
import matplotlib.pyplot as plt
from datetime import datetime
import graph_helper

start = datetime.now()

#import image
img = cv2.imread('signature2.PNG', 0)
img = cv2.resize(img, (960, 540))
ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

#thin image
thinned_image = ft.fastThin(img)

print("Time elapsed for thinning: " + str(datetime.now() - start))

#denoise image
denoised_image = cv2.fastNlMeansDenoising(thinned_image, h=40)

print("Time elapsed for denoising: " + str(datetime.now() - start))

cv2.imshow("Original Image with Threshold", img)

cv2.imshow("Thinned Image", thinned_image)

cv2.imshow("Denoised Image", denoised_image)

#convert image to points
pixel_coords, plot_x, plot_y = graph_helper.image_to_points(denoised_image)

pixel_coords.sort()

num_filtered_points = len(pixel_coords)

#Getting edges for graph
coordinate_point_graph = graph_helper.create_graph(pixel_coords, num_filtered_points)

print("Time elapsed for graph creation: " + str(datetime.now() - start))

#minimum spanning tree
connected_lines = graph_helper.minimum_spanning_graph(coordinate_point_graph)

connected_lines = graph_helper.reflect_over_diagonal(connected_lines, num_filtered_points)

print("Time elapsed for minimum spanning tree: " + str(datetime.now() - start))

graph_adjacency_list = graph_helper.adjacency_matrix_to_adjacency_list(connected_lines, num_filtered_points)

#print(graph_adjacency_list)

coordinate_order = []

#determine coordinate order
index = 0
curx = 0
cury = 0
while index < num_filtered_points:
    #starting points are at nodes with one edge
    if len(graph_adjacency_list[index]) != 1:
        index += 1
        continue
    #add the two points (When transitioning between lift pens, I want to move x and y directions separately

    while True:
        curx = pixel_coords[index][0]
        cury = abs(pixel_coords[index][1])
        coordinate_order.append((curx, cury))
        if len(graph_adjacency_list[index]) == 0:
            coordinate_order.append("Lift Pen")
            index = 0
            break
        next_point = graph_adjacency_list[index][0]
        graph_adjacency_list[index].remove(next_point)
        graph_adjacency_list[next_point].remove(index)
        index = next_point

print("Time elapsed for getting coordinate order: " + str(datetime.now() - start))


lift_pen_indices = [-1]
for i in range(len(coordinate_order)):
    if coordinate_order[i] == "Lift Pen":
        lift_pen_indices.append(i)

x_coords = []
y_coords = []

for i in range(len(lift_pen_indices) - 1):
    x_coords.append([x[0] for x in coordinate_order[lift_pen_indices[i] + 1: lift_pen_indices[i+1]]])
    y_coords.append([(-x[1]) for x in coordinate_order[lift_pen_indices[i] + 1: lift_pen_indices[i+1]]])

plt.ion()

for i in range(len(x_coords)):
    plt.plot(x_coords[i], y_coords[i], "k-")
    plt.pause(0.5)

f = open("coordinates.txt", "w")
f.write(str(coordinate_order))
f.close()

print(coordinate_order)
print(len(coordinate_order))

plt.show(block=True)
cv2.waitKey(0) # press any key to close
cv2.destroyAllWindows()

