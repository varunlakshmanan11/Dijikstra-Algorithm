# Importing Necessary libraries
import numpy as np
import matplotlib.pyplot as plt 
from queue import PriorityQueue
import cv2
import time

# Creating a empty canvas or map
map = np.ones((500, 1200, 3), dtype=np.uint8)*255

# Drawing shapes on the empty canvas with openCV to create a full map
rectangle1 = cv2.rectangle(map, pt1 = (100,500), pt2 = (175,100), color = (0 , 0,  0), thickness = -1) # Drawing rectangle1
clearence1 = cv2.rectangle(map, pt1 = (95,500), pt2 = (180,95), color = (0 , 255,  0), thickness = 5) #Clearance for rectangle1
rectangle2 = cv2.rectangle(map, pt1 = (275,0), pt2 = (350,400), color = (0 , 0,  0), thickness = -1) # Drawing rectangle2
clearence1 = cv2.rectangle(map, pt1 = (270,0), pt2 = (355,405), color = (0 , 255,  0), thickness = 5) # Clearance for rectangle 2

clearence3 = cv2.rectangle(map, pt1 = (895,45), pt2 = (1105,130), color = (0 , 255,  0), thickness = -1) # Clearance for rectangle3
clearence4 = cv2.rectangle(map, pt1 = (1015,125), pt2 = (1105,450), color = (0 , 255,  0), thickness = -1) # Clearance for rectangle4
clearence5 = cv2.rectangle(map, pt1 = (895,370), pt2 = (1105,455), color = (0 , 255,  0), thickness = -1) # Clearance for rectangle5

rectangle3 = cv2.rectangle(map, pt1 = (900,50), pt2 = (1100,125), color = (0 , 0,  0), thickness = -1) # Drawing rectangle3
rectangle4 = cv2.rectangle(map, pt1 = (1020,125), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1) # Drawing rectangle4
rectangle5 = cv2.rectangle(map, pt1 = (900,375), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1) # Drawing rectangle5
rectangle6 = cv2.rectangle(map, pt1 = (0,0), pt2 = (1205, 500), color = (0 , 255,  0), thickness = 5) # Defining border clearance

# Defining hexagon with coordinate points in the form of array.(connecting lines one by one)
hexagon = np.array([[500, 175],
                    [650, 100],
                    [800, 175], 
                    [800, 325], 
                    [650, 400],
                    [500, 325]
                    ])

hexagon = hexagon.reshape(-1,1,2)

# Defining the clearance for the hexagon in the form of array.(connecting lines one by one)
clearence_hexagon = np.array([[495, 170],
                              [645, 95],
                              [805, 170], 
                              [805, 330], 
                              [655, 405],
                              [495, 330]
                              ])

clearence_hexagon = clearence_hexagon.reshape(-1,1,2)

# Using Polylines to draw the hexagon using the array created.
cv2.polylines(map, [hexagon], isClosed = True, thickness = 4, color = (0, 0, 0))
# Filling the hexagon.
cv2.fillPoly(map, [hexagon], (0,0,0))
# Using Polylines to draw the clearance for the hexagon.
cv2.polylines(map, [clearence_hexagon], isClosed = True, thickness = 5, color = (0, 255, 0))
# Flipping the map
map = cv2.flip(map, flipCode = 0)
plt.imshow(map)
plt.show()

map = np.array(map)
# Initializing video writer
output_write = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('dijkstra_varun_lakshmanan.mp4', output_write, 30, (1200, 500))

## Defining 8 sets of functions to define action nodes.
# Function for moving up.
def action_up(node):
    x, y = node
    movement_up = x , y - 1
    n_x, n_y = movement_up
    return (n_x, n_y) 
# Function for moving down.
def action_down(node):
    x,  y = node
    movement_down = x , y + 1
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
    movement_upleft = x - 1, y - 1
    n_x, n_y = movement_upleft
    return (n_x, n_y)
#Function for moving upright.
def action_up_right(node):
    x, y = node
    movement_upright = x + 1, y - 1
    n_x, n_y = movement_upright
    return (n_x, n_y)
# Function for moving downleft.
def action_down_left(node):
    x, y = node
    movement_downleft = x - 1, y + 1
    n_x, n_y = movement_downleft
    return (n_x, n_y)
#Function for moving downright.
def action_down_right(node):
    x, y = node
    movement_downright = x + 1, y + 1 
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
           next_nodes.append((next_node, cost)) # Adding new nodes along with cost.
    
    return next_nodes
   
# Defining the function for dijkstra_algorithm to find the shortest distance between initial and goal node.
def dijkstra_path_planning(start_node,end_node):
    parent = {} # Creating a empty index to store parent nodes.
    cost_list = {start_node:0} # creating a cost_list to cost from each iteration.
    closedlist = set() # Closed list to keep track of visited elements.
    openlist = PriorityQueue() # Open List to store nodes that are to be visited.
    openlist.put((start_node,0)) #
    canvas_visualization = np.copy(map)
    step_count = 0
    while not openlist.empty():
        current_node, current_cost = openlist.get()
        closedlist.add(current_node)
        possible_states = possible_nodes(current_node, map)
        if current_node == end_node:
            path =  dijkstra_backtracking(parent, start_node, end_node, canvas_visualization, step_count)
            for _ in range(30):
                out.write(canvas_visualization)
            break
        
        for new_node, cost in possible_states:
            cost_to_come = current_cost + cost
            if new_node not in closedlist:
                if new_node not in cost_list or cost_to_come < cost_list[new_node]:
                    parent[new_node] = current_node
                    cost_list[new_node] = cost_to_come
                    new_cost = cost_to_come
                    openlist.put((new_node, new_cost))
                    cv2.circle(canvas_visualization, new_node, 2, (255, 0, 0), -1)
                    
                    if step_count % 1500 == 0:
                        out.write(canvas_visualization)
                    step_count += 1
        
    out.release()
    return path,None

def dijkstra_backtracking(parent, start_node, end_node, canvas_visualization,step_count):
    path = [end_node]
    while end_node != start_node:
        path.append(parent[end_node])
        end_node = parent[end_node]
    path.reverse()
    for node in path:
        cv2.circle(canvas_visualization, node, radius=2, color=(255, 0, 0), thickness=-1)
        if step_count % 20 == 0:
           out.write(canvas_visualization)
        step_count += 1    
    return path



def user_input(prompt,canvas):
  while True:
    try:  
        x, y = map(int, input(prompt).split())
        y_transform = canvas.shape[0]-y
        if x < 0 or y < 0 or x >= canvas.shape[1] or y >= canvas.shape[0]:
            print("Point is out of bounds!!!.Try again with a different values") 
        elif np.any(map[y_transform,x] != [255, 255, 255]):
            print("Node is in obstacle space")
        else:
            return x,y_transform
    except ValueError:
        print("Invalid Input. Please Enter in x y format")

x_initial, y_initial = user_input("Enter Initial Node as (x y): ", map)
x_goal, y_goal = user_input("Enter goal Node as (x y): ", map)
    
node_initial = (x_initial, y_initial)
node_goal = (x_goal, y_goal)

start = time.time()  

cv2.circle(map, node_initial, radius = 4 , color = (255, 255, 0), thickness = -1)
cv2.circle(map, node_goal, radius = 4 , color = (0, 255, 255), thickness = -1)
for _ in range(30):
    out.write(map)

path = dijkstra_path_planning(node_initial, node_goal)

end = time.time()
print('runtime',end - start)

                
             
    
        