# Importing Necessary libraries
import numpy as np
import matplotlib.pyplot as plt 
from queue import PriorityQueue
import cv2
import time

# Creating a empty space for canvas
Graph_map = np.ones((500, 1200, 3), dtype=np.uint8)*255

# Drawing rectangles on the white space with clearence.
cv2.rectangle(Graph_map, pt1 = (100,500), pt2 = (175,100), color = (0 , 0,  0), thickness = -1)
cv2.rectangle(Graph_map, pt1 = (95,500), pt2 = (180,95), color = (0 , 255,  0), thickness = 5)
cv2.rectangle(Graph_map, pt1 = (275,0), pt2 = (350,400), color = (0 , 0,  0), thickness = -1)
cv2.rectangle(Graph_map, pt1 = (270,0), pt2 = (355,405), color = (0 , 255,  0), thickness = 5)
cv2.rectangle(Graph_map, pt1 = (895,45), pt2 = (1105,130), color = (0 , 255,  0), thickness = -1)
cv2.rectangle(Graph_map, pt1 = (1015,125), pt2 = (1105,450), color = (0 , 255,  0), thickness = -1)
cv2.rectangle(Graph_map, pt1 = (895,370), pt2 = (1105,455), color = (0 , 255,  0), thickness = -1)
cv2.rectangle(Graph_map, pt1 = (900,50), pt2 = (1100,125), color = (0 , 0,  0), thickness = -1)
cv2.rectangle(Graph_map, pt1 = (1020,125), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1)
cv2.rectangle(Graph_map, pt1 = (900,375), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1)
cv2.rectangle(Graph_map, pt1 = (0,0), pt2 = (1200,500), color = (0 , 255,  0), thickness = 5)

# Drawing Hexagon on the White Space by putting the coordinates into a array. 
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

# Drawing Clearance matrix for Hexagon
clearence_hexagon = np.array([[495, 170],
                    [645, 95],
                    [805, 170], 
                    [805, 330], 
                    [655, 405],
                    [495, 330]

                   ])

clearence_hexagon = clearence_hexagon.reshape(-1,1,2)
clearence_hexagon

# Using OpenCV funtions to draw the hexagon and its clearance.
cv2.polylines(Graph_map, [hexagon], isClosed = True, thickness = 4, color = (0, 0, 0))
cv2.fillPoly(Graph_map, [hexagon], (0,0,0))
cv2.polylines(Graph_map, [clearence_hexagon], isClosed = True, thickness = 5, color = (0, 255, 0))
# Flipping the graph to match the coordinates required.
Graph_map = cv2.flip(Graph_map, flipCode = 0)

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
    openlist.put((0, start_node)) # Adding initial node into the open list.
    canvas_visualization = np.copy(Graph_map) # copying the graph map for visualization.
    step_count = 0 
    # While loop to perform the tasks of dijkstra's algorithm 
    while not openlist.empty():
        current_cost, current_node = openlist.get() # Getting Current cost and the current node from the openlist.
        closedlist.add(current_node) # Adding current node to the closed list.
        possible_states = possible_nodes(current_node, Graph_map) # calling function to get nodes to explore.
        # Checking whether current_node = goal_node, if the condition satisfies backtracking.
        if current_node == end_node:
            final_path = dijkstra_backtracking(parent, start_node, end_node, canvas_visualization, step_count) # Retruning the path
            for _ in range(30):
                out.write(canvas_visualization)
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
                    cv2.circle(canvas_visualization, new_node, 2, (255, 0, 0), -1)
                    if step_count%1500 == 0:
                        out.write(canvas_visualization)
                    step_count += 1
        
    out.release() 
    return None

# Defining function for backtracking to find path.
def dijkstra_backtracking(parent, start_node, end_node, canvas_visualization, step_count):
    path = [end_node] # Adding end node to the path
    while end_node != start_node: # If the end node is not equal to start_node, parent of the end_node is added to path and continues.
        path.append(parent[end_node])
        end_node = parent[end_node] # The parent of end node becomes the current node.
    path.reverse()
    # Visualizing Backtracking
    for j in range(1, len(path)):
        cv2.line(canvas_visualization, path[j - 1], path[j], (0, 0, 255), thickness=2) # Drawing lines to explore the path.
        if step_count % 15 == 0:
            out.write(canvas_visualization)
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
node_goal = (x_goal, y_goal)

start_time = time.time()   # Starting to check the runtime.
path = dijkstra_path_planning(node_initial, node_goal)
end_time = time.time()    # end of runtime
print(f'Runtime : {end_time-start_time}') # Printing the Runtime.
                
             
    
        
