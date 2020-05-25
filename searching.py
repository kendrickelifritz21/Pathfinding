from location import *


def initialize_closed_list(width, height):
    closed_list = []
    for y in range(height):
        closed_list.append([])
        for x in range(width):
            closed_list[y].append(False)
    return closed_list


def initialize_g_values(width, height):
    g_values = []
    for y in range(height):
        g_values.append([])
        for x in range(width):
            g_values[y].append(float('inf'))
    return g_values


class SearchNode:
    def __init__(self, location, parent):
        self.location = location
        self.parent = parent
        if parent:
            self.g_value = parent.g_value + 1
        else:
            self.g_value = 0


class AStarSearch:
    def __init__(self, grid):
        self.grid = grid
        self.open_list = []
        self.closed_list = initialize_closed_list(self.grid.width, self.grid.height)

    def search(self):
        start_node = SearchNode(self.grid.get_start_node_as_object, None)
        self.open_list.append(start_node)


        while self.open_list:
            lowest_f_value_node_index = self.find_lowest_f_value_node_index()
            self.expand_location(lowest_f_value_node_index)


    def find_lowest_f_value_node_index(self):
        lowest_f_value = float('-inf')
        lowest_f_value_node_index = None

        for index in range(len(self.open_list)):
            node = self.open_list[index]
            f_value = self.calculate_f_value(node)
            if lowest_f_value > f_value:
                lowest_f_value = f_value
                lowest_f_value_node_index = index
        return lowest_f_value_node_index


    def calculate_f_value(self, node):
        x, y = node.location.coordinates
        end_x, end_y = self.grid.get_end_node_as_pair()

        f_value = node.g_value + (abs(x - end_x) + abs(y - end_y))
        return f_value

    def expand_location(self, open_list_index):
        node = self.open_list.pop(open_list_index)
        # if node is end point, end loop
        # else
        # create successor nodes and add to open list
        # push parent node onto closed list

