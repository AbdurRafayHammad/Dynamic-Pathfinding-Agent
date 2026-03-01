# Dynamic-Pathfinding-Agent
A Python GUI-based Pathfinding Visualizer built using Tkinter that demonstrates how different search algorithms find paths in a grid environment.
Pathfinding Agent (A* & GBFS Visualizer)

This application allows users to:

Draw walls

Set start and goal positions

Generate random maps

Run A* and Greedy Best First Search (GBFS)

Visualize visited nodes and final path

Enable dynamic obstacles with automatic replanning

 Features
 Search Algorithms

A* (A-Star Search)

GBFS (Greedy Best First Search)

 Heuristics Supported

Manhattan Distance

Euclidean Distance

 Interactive Grid

Draw walls

Erase walls

Move Start position

Move Goal position

Resize grid (5x5 to 40x40)

Generate random maps

Clear walls

 Visualization

Visited nodes (Blue)

Final shortest path (Purple)

Animated agent movement (Cyan)

Dynamic obstacles (optional)

Automatic replanning when path is blocked

 Metrics Displayed

Nodes Visited

Path Cost

Execution Time (milliseconds)

 Technologies Used

Python 3.x

Tkinter (GUI)

Heapq (Priority Queue)

Math

Random

Time

▶ How to Run
1️⃣ Install Python

Make sure Python 3.x is installed.

Check version:

python --version
2️⃣ Run the Program
python 23F-0622_Q6.py

A grid setup dialog will appear where you can choose:

Rows (5–40)

Columns (5–40)

 How to Use
Step 1: Choose Grid Size

Set rows and columns in the setup window.

Step 2: Draw Environment

Use Draw Mode:

Wall → Add obstacles

Erase → Remove obstacles

Start → Move start node

Goal → Move goal node

Step 3: Choose Algorithm

From top bar:

Select A* or GBFS

Select heuristic (Manhattan / Euclidean)

Enable "Dynamic" if you want obstacles to appear during movement

Step 4: Run Search

Click  RUN

The agent will:

Explore nodes

Display visited cells

Highlight shortest path

Animate movement

Step 5: Stop (Optional)

Click ⬛ STOP to stop animation.

 Algorithm Overview
A* Algorithm

Uses:
f(n) = g(n) + h(n)

Guarantees optimal path (if heuristic is admissible)

Expands fewer nodes than uninformed search

Greedy Best First Search (GBFS)

Uses only heuristic:
f(n) = h(n)

Faster in some cases

Does NOT guarantee optimal path

 Color Legend
Color	Meaning
🟢 Green	Start Node
🔴 Red	Goal Node
⚫ Gray	Wall
🔵 Blue	Visited Node
🟣 Purple	Final Path
🔹 Cyan	Moving Agent
🔄 Dynamic Mode

When enabled:

Random walls may appear during agent movement

If a wall blocks the remaining path:

The agent automatically replans

Continues toward goal

This simulates real-world dynamic environments.

 Default Settings

Default Grid: 20x20

Default Wall Density: 30%

Animation Speed: 80ms per step

Obstacle Spawn Chance: 12%


 Limitations

Only 4-directional movement (Up, Down, Left, Right)

No diagonal movement

Dynamic replanning only triggers if new obstacle blocks remaining path
