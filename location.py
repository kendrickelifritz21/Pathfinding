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
        self.startPoint = None
        self.endPoint = None

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
            if coordinates != self.startPoint and coordinates != self.endPoint:
                widget.set_wall()
        except AttributeError:
            pass

    def reset_location_event_handler(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            if coordinates != self.startPoint and coordinates != self.endPoint:
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
            self.startPoint = coordinates
            if widget.is_wall():
                widget.reset_location()
            widget.config(bg="yellow")
            widget.type = LocationType.START
        except AttributeError:
            pass

    def get_start_point(self):
        return self.startPoint

    def set_end_event_handler(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            self.endPoint = coordinates
            if widget.is_wall():
                widget.reset_location()
            widget.config(bg="green")
            widget.type = LocationType.START
        except AttributeError:
            pass

    def get_end_point(self):
        return self.endPoint

    def reset_start_end(self):
        if self.startPoint:
            x, y = self.startPoint
            startLocation = self.locations[y][x]
            startLocation.config(bg="white")
            startLocation.type = LocationType.EMPTY
            self.startPoint = None
        if self.endPoint:
            x, y = self.endPoint
            endLocation = self.locations[y][x]
            endLocation.config(bg="white")
            endLocation.type = LocationType.EMPTY
            self.endPoint = None




class MyWindow(Tk):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.minsize(1350, 750)
        self.title("pathfinding")

        self.mazeGrid = LocationGrid(self, 50, 30)
        self.mazeGrid.pack(side=LEFT)

        self.buttonFrameContainer = Frame(master=self, relief=FLAT)
        self.buttonFrameContainer.pack(side=LEFT, fill=X, expand=True)

        self.button1 = Button(master=self.buttonFrameContainer, text="Start Point", bg="white")
        self.button1.bind("<Button-1>", self.start_point_button_clicked)
        self.button1.pack()

        self.button2 = Button(master=self.buttonFrameContainer, text="End Point", bg="white")
        self.button2.bind("<Button-1>", self.end_point_button_clicked)
        self.button2.pack()

        self.button3 = Button(master=self.buttonFrameContainer, text="Reset Start/End", bg="white")
        self.button3.bind("<Button-1>", self.reset_start_end_clicked)
        self.button3.pack()

    def start_point_button_clicked(self, event):
        if not self.mazeGrid.get_start_point():
            self.unbind_wall_setting()
            self.bind_start_point_setting()

    def end_point_button_clicked(self, event):
        if not self.mazeGrid.get_end_point():
            self.unbind_wall_setting()
            self.bind_end_point_setting()

    def reset_start_end_clicked(self, event):
        self.mazeGrid.reset_start_end()

    def unbind_wall_setting(self):
        for row in self.mazeGrid.locations:
            for location in row:
                location.unbind("<Button-1>")
                location.unbind("<Button-3>")
                location.unbind("<B1-Motion>")
                location.unbind("<B3-Motion>")

    def bind_wall_setting(self):
        for row in self.mazeGrid.locations:
            for location in row:
                location.bind("<Button-1>", self.mazeGrid.left_click_event_handler)
                location.bind("<Button-3>", self.mazeGrid.right_click_event_handler)
                location.bind("<B1-Motion>", self.mazeGrid.left_moved_event_handler)
                location.bind("<B3-Motion>", self.mazeGrid.right_moved_event_handler)

    def bind_start_point_setting(self):
        for row in self.mazeGrid.locations:
            for location in row:
                location.bind("<Button-1>", self.start_location_clicked)

    def start_location_clicked(self, event):
        self.mazeGrid.set_start_event_handler(event)
        self.bind_wall_setting()
        print(self.mazeGrid.get_start_point())

    def bind_end_point_setting(self):
        for row in self.mazeGrid.locations:
            for location in row:
                location.bind("<Button-1>", self.end_location_clicked)

    def end_location_clicked(self, event):
        self.mazeGrid.set_end_event_handler(event)
        self.bind_wall_setting()
        print(self.mazeGrid.get_end_point())
