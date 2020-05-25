from tkinter import *
from enum import Enum


class LocationType(Enum):
    EMPTY = 1
    WALL = 2
    START = 3
    END = 4


class Location(Frame):
    def __init__(self, master, x, y):
        super(Location, self).__init__(master, relief=SOLID, borderwidth=1, height=25, width=25, bg="white")
        self.type = LocationType.EMPTY
        self.coordinates = (x, y)
        self.neighbors = []

    def set_wall(self):
        self.config(bg="#383b39")
        self.type = LocationType.WALL
        #print(self.coordinates)
        #print("neighbors: ", self.neighbors, "\n")

    def reset_location(self):
        self.config(bg="white")
        self.type = LocationType.EMPTY

    def is_wall(self):
        return self.type is LocationType.WALL

    def add_neighbors(self, width, height):
        x, y = self.coordinates

        # add top neighbor if it exists
        if y - 1 >= 0:
            self.neighbors.append((x, y - 1))

        # add bottom neighbor if exists
        if y + 1 < height:
            self.neighbors.append((x, y + 1))

        # add left neighbor if exists
        if x - 1 >= 0:
            self.neighbors.append((x - 1, y))

        # add right neighbor if exists
        if x + 1 < width:
            self.neighbors.append((x + 1, y))



class LocationGrid(Frame):
    def __init__(self, master, width, height):
        super(LocationGrid, self).__init__(master)
        self.width = width
        self.height = height

        locations = []

        for y in range(height):
            locations.append([])
            for x in range(width):
                location = Location(self, x, y)
                location.grid(row=y, column=x)

                location.bind("<Button-1>", self.left_click_event_handler)
                location.bind("<Button-3>", self.right_click_event_handler)
                location.bind("<B1-Motion>", self.left_moved_event_handler)
                location.bind("<B3-Motion>", self.right_moved_event_handler)

                locations[y].append(location)

        self.locations = locations
        self.start_point = None
        self.end_point = None

        self.build_graph()

    def left_click_event_handler(self, event):
        self.set_wall_event_handler(event)

    def left_moved_event_handler(self, event):
        self.set_wall_event_handler(event)

    def right_click_event_handler(self, event):
        self.reset_location_event_handler(event)

    def right_moved_event_handler(self, event):
        self.reset_location_event_handler(event)

    def set_wall_event_handler(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            if coordinates != self.start_point and coordinates != self.end_point:
                widget.set_wall()
        except AttributeError:
            pass

    def reset_location_event_handler(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            if coordinates != self.start_point and coordinates != self.end_point:
                widget.reset_location()
        except AttributeError:
            pass

    def build_graph(self):
        for row in self.locations:
            for location in row:
                location.add_neighbors(self.width, self.height)

    def set_start_event_handler(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            self.start_point = coordinates
            if widget.is_wall():
                widget.reset_location()
            widget.config(bg="yellow")
            widget.type = LocationType.START
        except AttributeError:
            pass

    def get_start_point_as_pair(self):
        return self.start_point

    def get_start_point_as_object(self):
        start_x = self.start_point[0]
        start_y = self.start_point[1]

        return self.locations[start_y][start_x]

    def set_end_event_handler(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            self.end_point = coordinates
            if widget.is_wall():
                widget.reset_location()
            widget.config(bg="green")
            widget.type = LocationType.START
        except AttributeError:
            pass

    def get_end_point_as_pair(self):
        return self.end_point

    def get_end_point_as_object(self):
        end_x = self.end_point[0]
        end_y = self.end_point[1]

        return self.locations[end_y][end_x]

    def reset_start_end(self):
        if self.start_point:
            x, y = self.start_point
            start_location = self.locations[y][x]
            start_location.config(bg="white")
            start_location.type = LocationType.EMPTY
            self.start_point = None
        if self.end_point:
            x, y = self.end_point
            end_location = self.locations[y][x]
            end_location.config(bg="white")
            end_location.type = LocationType.EMPTY
            self.end_point = None

    def get_point_as_object(self, x, y):
        return self.locations[y][x]


class ButtonContainer(Frame):
    def __init__(self, master):
        super(ButtonContainer, self).__init__(master, relief=FLAT)

        self.button_manager = None

        self.button1 = Button(master=self, text="Start Point", bg="white")
        self.button1.bind("<Button-1>", self.start_point_button_clicked)
        self.button1.pack()

        self.button2 = Button(master=self, text="End Point", bg="white")
        self.button2.bind("<Button-1>", self.end_point_button_clicked)
        self.button2.pack()

        self.button3 = Button(master=self, text="Reset Start/End", bg="white")
        self.button3.bind("<Button-1>", self.reset_start_end_clicked)
        self.button3.pack()

    def start_point_button_clicked(self, event):
        self.button_manager.start_point_button_clicked()

    def end_point_button_clicked(self, event):
        self.button_manager.end_point_button_clicked()

    def reset_start_end_clicked(self, event):
        self.button_manager.reset_start_end_clicked()


class Window(Tk):
    def __init__(self):
        super(Window, self).__init__()

        self.minsize(1350, 750)
        self.title("pathfinding")

        self.grid = LocationGrid(self, 50, 30)
        self.grid.pack(side=LEFT)

        self.button_container = ButtonContainer(self)
        self.button_container.pack(side=LEFT, fill=X, expand=True)

    def unbind_wall_setting(self):
        for row in self.grid.locations:
            for location in row:
                location.unbind("<Button-1>")
                location.unbind("<Button-3>")
                location.unbind("<B1-Motion>")
                location.unbind("<B3-Motion>")

    def bind_wall_setting(self):
        for row in self.grid.locations:
            for location in row:
                location.bind("<Button-1>", self.grid.left_click_event_handler)
                location.bind("<Button-3>", self.grid.right_click_event_handler)
                location.bind("<B1-Motion>", self.grid.left_moved_event_handler)
                location.bind("<B3-Motion>", self.grid.right_moved_event_handler)

    def bind_start_point_setting(self):
        for row in self.grid.locations:
            for location in row:
                location.bind("<Button-1>", self.start_location_clicked)

    def start_location_clicked(self, event):
        self.grid.set_start_event_handler(event)
        self.bind_wall_setting()
        print(self.grid.get_start_point_as_pair())

    def bind_end_point_setting(self):
        for row in self.grid.locations:
            for location in row:
                location.bind("<Button-1>", self.end_location_clicked)

    def end_location_clicked(self, event):
        self.grid.set_end_event_handler(event)
        self.bind_wall_setting()
        print(self.grid.get_end_point_as_pair())


class ButtonManager:
    def __init__(self, window):
        self.window = window
        self.window.button_container.button_manager = self

    def start_point_button_clicked(self):
        if not self.window.grid.get_start_point_as_pair():
            self.window.unbind_wall_setting()
            self.window.bind_start_point_setting()

    def end_point_button_clicked(self):
        if not self.window.grid.get_end_point_as_pair():
            self.window.unbind_wall_setting()
            self.window.bind_end_point_setting()

    def reset_start_end_clicked(self):
        self.window.grid.reset_start_end()
