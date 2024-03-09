import numpy as np
import matplotlib.pyplot as plt 
from queue import PriorityQueue
import cv2


empty_canvas = np.ones((500, 1200, 3))

rectangle1 = cv2.rectangle(empty_canvas, pt1 = (100,500), pt2 = (175,100), color = (0 , 0,  0), thickness = -1)
clearence1 = cv2.rectangle(empty_canvas, pt1 = (95,500), pt2 = (180,95), color = (0 , 255,  0), thickness = 5)
rectangle2 = cv2.rectangle(empty_canvas, pt1 = (275,0), pt2 = (350,400), color = (0 , 0,  0), thickness = -1)
clearence1 = cv2.rectangle(empty_canvas, pt1 = (270,0), pt2 = (355,405), color = (0 , 255,  0), thickness = 5)

clearence3 = cv2.rectangle(empty_canvas, pt1 = (895,45), pt2 = (1105,130), color = (0 , 255,  0), thickness = -1)
clearence4 = cv2.rectangle(empty_canvas, pt1 = (1015,125), pt2 = (1105,450), color = (0 , 255,  0), thickness = -1)
clearence5 = cv2.rectangle(empty_canvas, pt1 = (895,370), pt2 = (1105,455), color = (0 , 255,  0), thickness = -1)

rectangle3 = cv2.rectangle(empty_canvas, pt1 = (900,50), pt2 = (1100,125), color = (0 , 0,  0), thickness = -1)
rectangle4 = cv2.rectangle(empty_canvas, pt1 = (1020,125), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1)
rectangle5 = cv2.rectangle(empty_canvas, pt1 = (900,375), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1)
rectangle6 = cv2.rectangle(empty_canvas, pt1 = (5,5), pt2 = (1195,495), color = (0 , 255,  0), thickness = 5)

hexagon = np.array([[500, 175],
                    [650, 100],
                    [800, 175], 
                    [800, 325], 
                    [650, 400],
                    [500, 325]

                   ])
print(hexagon.shape)
hexagon = hexagon.reshape(-1,1,2)
hexagon

clearence_hexagon = np.array([[495, 170],
                    [645, 95],
                    [805, 170], 
                    [805, 330], 
                    [655, 405],
                    [495, 330]

                   ])

clearence_hexagon = clearence_hexagon.reshape(-1,1,2)
clearence_hexagon

cv2.polylines(empty_canvas, [hexagon], isClosed = True, thickness = 4, color = (0, 0, 0))
cv2.fillPoly(empty_canvas, [hexagon], (0,0,0))
cv2.polylines(empty_canvas, [clearence_hexagon], isClosed = True, thickness = 5, color = (0, 255, 0))
empty_canvas = cv2.flip(empty_canvas, flipCode = 0)
plt.imshow(empty_canvas)
plt.show()

empty_canvas = np.array(empty_canvas)
action_set = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]

def action_up(node):
    x, y = node
    movement_up = x , y + 1
    n_x, n_y = movement_up
    return (n_x, n_y) 

def action_down(node):
    x,  y = node
    movement_down = x , y - 1
    n_x, n_y = movement_down
    return (n_x, n_y)

def action_left(node):
    x, y = node 
    movement_left = x - 1 , y 
    n_x, n_y = movement_left
    return (n_x, n_y)
def action_right(node):
    x, y = node
    movement_right = x + 1, y
    n_x, n_y = movement_right
    return (n_x, n_y)

def action_up_left(node):
    x, y = node
    movement_upleft = x - 1, y + 1
    n_x, n_y = movement_upleft
    return (n_x, n_y)

def action_up_right(node):
    x, y = node
    movement_upright = x + 1, y + 1
    n_x, n_y = movement_upright
    return (n_x, n_y)

def action_down_left(node):
    x, y = node
    movement_downleft = x - 1, y - 1
    n_x, n_y = movement_downleft
    return (n_x, n_y)

def action_down_right(node):
    x, y = node
    movement_downright = x + 1, y - 1 
    n_x, n_y = movement_downright
    return (n_x, n_y)

def possible_nodes(node,empty_canvas):
    action_set = {action_up: 1,
                  action_down: 1,
                  action_left: 1,
                  action_right: 1 ,
                  action_up_left: 1.4,
                  action_up_right: 1.4,
                  action_down_left: 1.4,
                  action_down_right: 1.4}
    
    
    rows, columns, _ = empty_canvas.shape
    next_nodes = []
    for movement, cost in action_set.items():
        next_node = movement(node)
        next_x,next_y = next_node
        next_cost = cost
        if 0 <= next_x < columns and 0 <= next_y < rows and np.all(empty_canvas[next_y,next_x] == [1, 1, 1]):
            if next_node not in next_nodes:
                next_nodes.append((next_node, cost))
    
    return next_nodes

def dijkstra_backtracking(parent, start_node, end_node):
    path = [end_node]
    
    while end_node != start_node:
        path.append(parent[end_node])
        end_node = parent[end_node]
    path.reverse()
    return path

def dijkstra_path_planning(start_node,end_node):
    parent = {}
    cost_list = {start_node:0}
    closedlist = []
    openlist = PriorityQueue()
    openlist.put((start_node,0))
    while not openlist.empty():
        current_node, current_cost = openlist.get()
        closedlist.append(current_node)
        possible_states = possible_nodes(current_node, empty_canvas)
        if current_node == end_node:
            return dijkstra_backtracking(parent, start_node, end_node)
        
        for new_node, cost in possible_states:
            cost_to_come = current_cost + cost
            if new_node not in closedlist:
                if new_node not in cost_list or cost_to_come < cost_list[new_node]:
                    parent[new_node] = current_node
                    cost_list[new_node] = cost_to_come
                    new_cost = cost_to_come
                    openlist.put((new_node, new_cost))
            

    return None

                
             
    
        
