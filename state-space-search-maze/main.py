from src.exception.no_path_found_exception import NoPathFoundException
from src.input_parser import InputParser, MODE
import src.maze as m
from src.navigator.navigator import get_solver
from src.visualiser.visualiser import Visualiser


def main():
    parser = InputParser()
    mode = parser.get_data()[MODE]
    maze = m.Builder(parser.get_data()).build()
    path, history = get_solver(mode)(maze).solve()

    try:
        Visualiser(path, history, maze).draw()
    except NoPathFoundException as e:
        print("No path has been found.")
        print(e.history)


if __name__ == "__main__":
    main()
