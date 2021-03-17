import curses
import time

from src.config import DRAW_DELAY, CLOSED_VERTEX, PATH_VERTEX, WALL, STARTING_VERTEX, ENDING_VERTEX
from src.maze import Maze


class Visualiser:
    """
    A class that draws the maze and navigation through it to the console

    Attributes
    ----------
    path: list
        Sequence of vertices from start to finish
    visited_nodes:
        All opened nodes
    start: str
        Coordinates of the starting position
    end: str
        Coordinates of the target position

    """

    def __init__(self, path, visited_nodes, maze: Maze):
        self.path = path
        self.visited_nodes = visited_nodes
        self.maze = maze
        self.start = str(self.maze.start)
        self.end = str(self.maze.end)

    def draw(self):
        """
        Draws all the information to the console
        :return: None
        """
        self.__setup_curses()

        self.__draw_maze()
        self.__draw_path(self.visited_nodes, CLOSED_VERTEX)
        self.__draw_path(self.path, PATH_VERTEX)
        self.__write_stats()
        self.screen.getkey()
        self.__finish_curses()

    def __draw_vertex(self, vertex: str, symbol: str):
        """
        Draws a symbol on the screen at specific coordinates
        :param vertex: Vertex to draw the symbol at
        :param symbol: Symbol to draw
        :return: None
        """
        x, y = vertex.split(',')
        try:
            self.screen.addstr(int(x), int(y), symbol)
        except curses.error:
            pass

    def __draw_vertices(self, vertices, symbol):
        """
        Draws a collection of vertices
        :return: None
        """
        for vertex in vertices:
            self.__draw_vertex(vertex, symbol)
        self.__refresh()

    def __finish_curses(self):
        """
        Closes curses and resets console's parameters
        :return: None
        """
        curses.nocbreak()
        curses.echo()
        self.screen.keypad(True)
        curses.endwin()

    def __draw_maze(self):
        """
        Draws the maze - walls and starting and ending point
        :return: None
        """
        self.__draw_vertices(self.__get_walls(), WALL)
        self.__draw_vertex(self.start, STARTING_VERTEX)
        self.__draw_vertex(self.end, ENDING_VERTEX)
        self.__refresh()

    def __draw_path(self, path, symbol):
        """
        Draws the path from start to finish
        :return: None
        """
        for vertex in path:
            if vertex == self.start or vertex == self.end:
                continue
            self.__draw_vertex(vertex, symbol)
            self.__refresh()
            time.sleep(DRAW_DELAY)

    def __get_walls(self):
        return self.maze.walls

    def __get_end(self):
        return self.maze.end

    def __get_start(self):
        return self.maze.start

    def __setup_curses(self):
        """
        Prepares curses and the console for drawing
        :return: None
        """
        self.screen = curses.initscr()
        self.screen.keypad(False)
        self.screen.clear()
        curses.noecho()
        curses.cbreak()

    def __refresh(self):
        self.screen.refresh()

    def __write_stats(self):
        """
        Writes the result information to the console
        :return: None
        """
        x, y = 0, int(self.maze.height)
        stats = ['-' * self.maze.width,
                 STARTING_VERTEX + '   Start',
                 ENDING_VERTEX + '   End',
                 CLOSED_VERTEX + '   Opened node',
                 PATH_VERTEX + '   Path',
                 WALL + '   Wall',
                 "' '" + ' Fresh node',
                 '-' * self.maze.width,
                 'Nodes expanded: ' + str(len(self.visited_nodes)),
                 'Path length: ' + str(len(self.path)),
                 '-' * self.maze.width,
                 'Press any key to exit ...'
                 ]
        try:
            for stat in stats:
                self.screen.addstr(y, x, stat)
                y += 1
            self.__refresh()
        except curses.error:
            pass
