# Importing Necessary libraries.
import numpy as np
import matplotlib.pyplot as plt 
from queue import PriorityQueue
import cv2
import time

# Creating a empty space for drawing graph.
Graph_map = np.ones((500, 1200, 3), dtype=np.uint8)*255

# Center of the hexagon.
center_h = (650,250)
# Side of hexagon.
side = 150
# radius from thhe center.
r = np.cos(np.pi/6) * side
# Center Coordinates of hexagon.
c_x,c_y = center_h

angles = np.linspace(np.pi / 2, 2 * np.pi + np.pi / 2, 7)[:-1]
v_x = c_x + r * np.cos(angles) # x_coordinate_vertices.
v_y = c_y + r * np.sin(angles) # y_coordinate_vertices.
radius_clearance = r + 5 # Clearance from radius.
v_x_c = c_x + radius_clearance * np.cos(angles) # x_coordinate_clearance_vertices.
v_y_c= c_y + radius_clearance * np.sin(angles) # y_coordinate_clearance_vertices.
vertices = np.vstack((v_x, v_y)).T # storing x and y vertices in a tuple.
clearance_verticies = np.vstack((v_x_c, v_y_c)).T # storing clearance x and y vertices.

# Drawaing objects on the empty_space by iterating in for loop using half plane equations.
for x in range(1200):
    for y in range(500):
        y_transform = 500 - y

        # Wall clearance.
        if (x <= 5 or x >= 1195 or y_transform <= 5 or y_transform >= 495):
            Graph_map[y,x] = [0,255,0]
        
        # object 1(rectangle)
        if (x >= 100 and x <= 175  and y_transform >= 100 and y_transform <= 500 ):
            Graph_map[y,x] = [0,0,0]
        elif (x >= 100 - 5  and x <= 175 + 5 and y_transform >= 100 - 5 and y_transform <= 500 + 5):
            Graph_map[y,x] = [0, 255, 0]
        
        # object 2(rectangle)
        if (x >= 275 and x <= 350 and y_transform >= 0 and y_transform <= 400):
            Graph_map[y,x] = [0,0,0]
        elif(x >= 275 - 5 and x <= 350 + 5 and y_transform >= 0 - 5 and y_transform <= 400 + 5):
             Graph_map[y,x] = [0, 255, 0] 

        # object 3 (combination of 3 rectangles)
        if (x >= 1020 - 5 and x <= 1100 + 5 and y_transform>= 50 - 5  and y_transform <= 450 + 5):
            Graph_map[y,x] = [0,255,0]
        elif (x >= 900 - 5  and x <= 1100 + 5  and y_transform >= 50 - 5 and y_transform <= 125 + 5):
            Graph_map[y,x] = [0, 255, 0]
        elif (x >= 900 - 5 and x <= 1100 + 5 and y_transform >= 375 - 5 and y_transform <= 450 + 5):
            Graph_map[y,x] = [0,255,0]
        
        if (x >= 1020 and x <= 1100 and y_transform>= 50  and y_transform <= 450 ):
            Graph_map[y,x] = [0,0,0]
        elif (x >= 900 and x <= 1100  and y_transform >= 50 and y_transform <= 125):
            Graph_map[y,x] = [0,0,0]
        elif (x >= 900 and x <= 1100 and y_transform >= 375 and y_transform <= 450):
            Graph_map[y,x] = [0,0,0]
        
# object 4 (hexagon)
def hexagon(x, y, vertices): # Defining a function to calucalate cross product of vertices inside hexagon.
    result = np.zeros(x.shape, dtype=bool)
    num_vertices = len(vertices)
    for i in range(num_vertices):
        j = (i + 1) % num_vertices
        cross_product = (vertices[j, 1] - vertices[i, 1]) * (x - vertices[i, 0]) - (vertices[j, 0] - vertices[i, 0]) * (y - vertices[i, 1])
        result |= cross_product > 0
    return ~result


x, y = np.meshgrid(np.arange(1200), np.arange(500))

hexagon_original = hexagon(x, y, vertices)
hexagon_clearance = hexagon(x, y,clearance_verticies) & ~hexagon_original

# Drawing hexagon and its clearance on the graph_map.
Graph_map[hexagon_clearance] = [0, 255, 0]
Graph_map[hexagon_original] = [0, 0, 0]

# Video Writer is initialized.
output_write = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('dijkstra_varun_lakshmanan.mp4', output_write, 30, (1200, 500))

## Defining 8 sets of functions to define action nodes.

# Function for moving up.
def action_up(node):
    x, y = node
    movement_up = x , y + 1
    n_x, n_y = movement_up
    return (n_x, n_y) 

# Function for moving down.
def action_down(node):
    x,  y = node
    movement_down = x , y - 1
    n_x, n_y = movement_down
    return (n_x, n_y)
# Function for moving left.
def action_left(node):
    x, y = node 
    movement_left = x - 1 , y 
    n_x, n_y = movement_left
    return (n_x, n_y)
# Function for moving right.
def action_right(node):
    x, y = node
    movement_right = x + 1, y
    n_x, n_y = movement_right
    return (n_x, n_y)
# Function for moving upleft.
def action_up_left(node):
    x, y = node
    movement_upleft = x - 1, y + 1
    n_x, n_y = movement_upleft
    return (n_x, n_y)
#Function for moving upright.
def action_up_right(node):
    x, y = node
    movement_upright = x + 1, y + 1
    n_x, n_y = movement_upright
    return (n_x, n_y)
# Function for moving downleft.
def action_down_left(node):
    x, y = node
    movement_downleft = x - 1, y - 1
    n_x, n_y = movement_downleft
    return (n_x, n_y)
#Function for moving downright.
def action_down_right(node):
    x, y = node
    movement_downright = x + 1, y - 1 
    n_x, n_y = movement_downright
    return (n_x, n_y)

# Defining a function to get possible nodes. 
def possible_nodes(node,empty_canvas):
    # Setting up a dictionary to store action function as key and cost as value.
    action_set = {action_up: 1,
                  action_down: 1,
                  action_left: 1,
                  action_right: 1 ,
                  action_up_left: 1.4,
                  action_up_right: 1.4,
                  action_down_left: 1.4,
                  action_down_right: 1.4}
    
    
    rows, columns, _ = empty_canvas.shape 
    next_nodes = [] # Creating a empty list for storing new nodes
    for movement, cost in action_set.items(): # For loop for getting each action and cost from the dictionary
        next_node = movement(node)
        next_x,next_y = next_node
        # Checking condition to check if the node is on the obstracle.
        if 0 <= next_x < columns and 0 <= next_y < rows and np.all(empty_canvas[next_y,next_x] == [255, 255, 255]):
            if next_node not in next_nodes: # Checking if the node is already visited.
                next_nodes.append((cost, next_node)) # Adding the possible nodes to the list.
    
    return next_nodes

# Defining function for performing dijkstra's algorithm to find the shortest distance between initial and final node.
def dijkstra_path_planning(start_node,end_node):
    parent = {} # Empty dictionary for parent node is created.
    cost_list = {start_node:0} # Cost is stored in each iteration.
    closedlist = set() # Defining closedlist to keep track of explored nodes.
    openlist = PriorityQueue() # openlist contains node to be explored.
    openlist.put((start_node, 0)) # Adding initial node into the open list.
    map_visualization = np.copy(Graph_map) # copying the graph map for visualization.
    step_count = 0 
    # While loop to perform the tasks of dijkstra's algorithm 
    while not openlist.empty():
        current_node, current_cost = openlist.get() # Getting Current cost and the current node from the openlist.
        closedlist.add(current_node) # Adding current node to the closed list.
        possible_states = possible_nodes(current_node, Graph_map) # calling function to get nodes to explore.
        # Checking whether current_node = goal_node, if the condition satisfies backtracking.
        if current_node == end_node:
            final_path = dijkstra_backtracking(parent, start_node, end_node, map_visualization, step_count) # Retruning the path
            for _ in range(30):
                out.write(map_visualization)
            break
        # For loop to explore the possible nodes.
        for cost, new_node in possible_states:
            cost_to_come = current_cost + cost 
            if new_node not in closedlist:
                if new_node not in cost_list or cost_to_come < cost_list[new_node]:
                    parent[new_node] = current_node
                    cost_list[new_node] = cost_to_come
                    new_cost = cost_to_come
                    openlist.put((new_node, new_cost))
                    # Visualizing Node Exploration and writing the frames to the video.
                    cv2.circle(map_visualization, new_node, 2, (255, 0, 0), -1)
                    if step_count%1500 == 0:
                        out.write(map_visualization)
                    step_count += 1
        
    out.release() 
    return None

# Defining function for backtracking to find path.
def dijkstra_backtracking(parent, start_node, end_node, map_visualization, step_count):
    path = [end_node] # Adding end node to the path
    while end_node != start_node: # If the end node is not equal to start_node, parent of the end_node is added to path and continues.
        path.append(parent[end_node])
        end_node = parent[end_node] # The parent of end node becomes the current node.
    path.reverse()
    # Visualizing Backtracking
    for j in range(1, len(path)):
        cv2.line(map_visualization, path[j - 1], path[j], (0, 0, 255), thickness=2) # Drawing lines to explore the path.
        if step_count % 15 == 0:
            out.write(map_visualization)
        step_count +=1
    return path

# Defining function to get input from the user by checking the presence of the input node in the obstacle space.
def user_input(prompt,canvas):
  while True:
    try:  
        x, y = map(int, input(prompt).split()) # Getting Input from the user
        y_transform = canvas.shape[0]-y # fliping y - coordinate to match the origin required.
        if x < 0 or y < 0 or x >= canvas.shape[1] or y >= canvas.shape[0]: # Checking if x or y is out of graph.
            print("Point is out of bounds!!!.Try again with a different values") 
        elif np.any(Graph_map[y_transform,x] != [255, 255, 255]): # checking whether the nodes are on the obstacle space.
            print("Node is in obstacle space")
        else:
            return x,y_transform # Retruning x and y_transform.
    except ValueError:
        print("Invalid Input. Please Enter in x y format")

x_initial, y_initial = user_input("Enter Initial Node as (x y): ", Graph_map) # Getting initial coordinates by calling the function.
x_goal, y_goal = user_input("Enter goal Node as (x y): ", Graph_map) # Getting goal coordinates by calling the function.
    
node_initial = (x_initial, y_initial)
print(f'initial_node : {node_initial}')
node_goal = (x_goal, y_goal)
print(f'Goal_node : {node_goal}')


start_time = time.time()   # Starting to check the runtime.
path = dijkstra_path_planning(node_initial, node_goal)
end_time = time.time()    # end of runtime
print(f'Runtime : {end_time-start_time}, seconds') # Printing the Runtime.
                
             
    
        
