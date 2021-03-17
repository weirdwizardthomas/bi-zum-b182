# Maze navigator
Maze navigator is a Python 3 programme that utilises various state space search algorithms to navigate a maze.

## Required packages
To run, the programme requires following packages to be installed:
1. numPy
1. curses

## Running the programme
To run the programme, provide a maze (e.g. mazes in the `/data` folder) and the keyword representing one of the algorithms below.
```
python3 main.py ./data/devel/36.txt BFS
```
## Input
The programme reads mazes from a text file, where `X`  and ` ` (space) represent a wall and a space(traverseable spot), respectively. After the maze itself is read, the programme also expects starting and ending vertices to follow in the file.

Below is an example of a simple maze:
```
XXX
X X
XXX
start 1, 1
end 1, 1
```

## Algorithms
The programme utilises a range of searching algorithms, which can be called by their respective abbreviations listed below:

| Keyword | Algorithm |
| ------------- |:-------------:|
| BFS| Breadth First Search |
| DFS| Depth First Search |
| Random| Random Search |
| Dijkstra| Dijkstra's Shortest Path First |
| Greedy| Greedy Search |
| A*| A* Search |