from location import *
import time


def initialize_closed_list(width, height):
    closed_list = []
    for y in range(height):
        closed_list.append([])
        for x in range(width):
            closed_list[y].append(False)
    return closed_list


class SearchNode:
    def __init__(self, location, parent):
        self.location = location
        self.parent = parent
        if parent:
            self.g_value = parent.g_value + 1
        else:
            self.g_value = 0


class AStarSearch:
    def __init__(self, grid, window):
        self.window = window
        self.grid = grid
        self.open_list = {}
        self.closed_list = initialize_closed_list(self.grid.width, self.grid.height)
        self.end_point_found = False

    def search(self):
        start_node = SearchNode(self.grid.get_start_point_as_object(), None)
        self.open_list[start_node.location.coordinates] = start_node
        current_node = None

        while self.open_list and not self.end_point_found:
            lowest_f_value_node_index = self.find_lowest_f_value_node_index()
            current_node = self.expand_location(lowest_f_value_node_index)
            time.sleep(0.1)

        while current_node.parent:
            if current_node.location.type == "empty":
                current_node.location.config(bg="#8367C7")
            current_node = current_node.parent

    def find_lowest_f_value_node_index(self):
        lowest_f_value = float('inf')
        lowest_f_value_key = None

        for key, node in self.open_list.items():
            f_value = self.calculate_f_value(node)
            if lowest_f_value > f_value:
                lowest_f_value = f_value
                lowest_f_value_key = node.location.coordinates
        return lowest_f_value_key

    def calculate_f_value(self, node):
        x, y = node.location.coordinates
        end_x, end_y = self.grid.get_end_point_as_pair()

        f_value = node.g_value + (abs(x - end_x) + abs(y - end_y))
        return f_value

    def expand_location(self, open_list_index):
        node = self.open_list.pop(open_list_index)
        # if node is end point, end loop
        if node.location.type == "end":
            self.end_point_found = True
        # else
        else:
            # create successor nodes and add to open list
            for successor in node.location.neighbors:
                x, y = successor
                if not self.closed_list[y][x] and self.grid.locations[y][x].type != "wall":
                    successor_node = SearchNode(self.grid.get_point_as_object(x, y), node)
                    coordinates = successor_node.location.coordinates

                    if coordinates in self.open_list:
                        current_f_value = self.calculate_f_value(self.open_list[coordinates])
                        if self.calculate_f_value(successor_node) < current_f_value:
                            self.open_list[coordinates] = successor_node
                    else:
                        self.open_list[coordinates] = successor_node
        # push parent node onto closed list
        if node.location.type == "empty":
            node.location.config(bg="#F7B801")
            self.window.update()
        x, y = node.location.coordinates
        self.closed_list[y][x] = True
        return node

