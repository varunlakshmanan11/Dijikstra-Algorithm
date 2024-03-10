import numpy as np
import matplotlib.pyplot as plt 
from queue import PriorityQueue
import cv2


empty_canvas = np.ones((500, 1200, 3), dtype=np.uint8)*255

rectangle1 = cv2.rectangle(empty_canvas, pt1 = (100,500), pt2 = (175,100), color = (0 , 0,  0), thickness = -1)
clearence1 = cv2.rectangle(empty_canvas, pt1 = (95,500), pt2 = (180,95), color = (0 , 255,  0), thickness = 5)
rectangle2 = cv2.rectangle(empty_canvas, pt1 = (275,0), pt2 = (350,400), color = (0 , 0,  0), thickness = -1)
clearence2 = cv2.rectangle(empty_canvas, pt1 = (270,0), pt2 = (355,405), color = (0 , 255,  0), thickness = 5)

clearence3 = cv2.rectangle(empty_canvas, pt1 = (895,45), pt2 = (1105,130), color = (0 , 255,  0), thickness = -1)
clearence4 = cv2.rectangle(empty_canvas, pt1 = (1015,125), pt2 = (1105,450), color = (0 , 255,  0), thickness = -1)
clearence5 = cv2.rectangle(empty_canvas, pt1 = (895,370), pt2 = (1105,455), color = (0 , 255,  0), thickness = -1)

rectangle3 = cv2.rectangle(empty_canvas, pt1 = (900,50), pt2 = (1100,125), color = (0 , 0,  0), thickness = -1)
rectangle4 = cv2.rectangle(empty_canvas, pt1 = (1020,125), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1)
rectangle5 = cv2.rectangle(empty_canvas, pt1 = (900,375), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1)
rectangle6 = cv2.rectangle(empty_canvas, pt1 = (0,0), pt2 = (1200,500), color = (0 , 255,  0), thickness = 5)

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
# Initialize video writer
output_write = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('path_planning_visualization.mp4', output_write, 30, (1200, 500))

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
        if 0 <= next_x < columns and 0 <= next_y < rows and np.all(empty_canvas[next_y,next_x] == [255, 255, 255]):
            if next_node not in next_nodes:
                next_nodes.append((next_node, cost))
    
    return next_nodes

def dijkstra_backtracking(parent, start_node, end_node, canvas_visualization, step_count):
    path = [end_node]
    
    while end_node != start_node:
        path.append(parent[end_node])
        end_node = parent[end_node]
    path.reverse()
    for j in range(1, len(path)):
        cv2.line(canvas_visualization, path[j - 1], path[j], (0, 0, 255), thickness=2)
        if step_count % 15 == 0:
            out.write(canvas_visualization)
        step_count +=1

    return path
   

def dijkstra_path_planning(start_node,end_node):
    parent = {}
    cost_list = {start_node:0}
    closedlist = set()
    openlist = PriorityQueue()
    openlist.put((start_node,0))
    canvas_visualization = np.copy(empty_canvas)
    step_count = 0
    while not openlist.empty():
        current_node, current_cost = openlist.get()
        closedlist.add(current_node)
        possible_states = possible_nodes(current_node, empty_canvas)
        if current_node == end_node:
            final_path = dijkstra_backtracking(parent, start_node, end_node, canvas_visualization)
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
                    
                    if step_count%3000 == 0:
                        out.write(canvas_visualization)
                    step_count += 1
        
    out.release()
    return None

def user_input(prompt,canvas):
  while True:
    try:  
        x, y = map(int, input(prompt).split())
        y_transform = canvas.shape[0]-y
        if x < 0 or y < 0 or x >= canvas.shape[1] or y >= canvas.shape[0]:
            print("Point is out of bounds!!!.Try again with a different values") 
        elif np.any(empty_canvas[y_transform,x] != [255, 255, 255]):
            print("Node is in obstacle space")
        else:
            return x,y_transform
    except ValueError:
        print("Invalid Input. Please Enter in x y format")

x_initial, y_initial = user_input("Enter Initial Node as (x y): ", empty_canvas)
x_goal, y_goal = user_input("Enter goal Node as (x y): ", empty_canvas)
    
node_initial = (x_initial, y_initial)
node_goal = (x_goal, y_goal)
    
path = dijkstra_path_planning(node_initial, node_goal)