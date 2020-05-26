from tkinter import *
from searching import *


class Location(Frame):
    def __init__(self, master, x, y):
        super(Location, self).__init__(master, relief=SOLID, borderwidth=1, height=25, width=25, bg="white")
        self.type = "empty"
        self.coordinates = (x, y)
        self.neighbors = []

    def set_wall(self):
        self.config(bg="#757372")
        self.type = "wall"

    def reset_location(self):
        self.config(bg="white")
        self.type = "empty"

    def is_wall(self):
        return self.type == "wall"

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
            if widget.is_wall():
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
            widget.config(bg="#4361EE")
            widget.type = "start"
        except AttributeError:
            pass

    def get_start_point_as_pair(self):
        return self.start_point

    def get_start_point_as_object(self):
        if self.start_point:
            start_x = self.start_point[0]
            start_y = self.start_point[1]

            return self.locations[start_y][start_x]
        else:
            return None

    def set_end_event_handler(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            self.end_point = coordinates
            if widget.is_wall():
                widget.reset_location()
            widget.config(bg="#4CC9F0")
            widget.type = "end"
        except AttributeError:
            pass

    def get_end_point_as_pair(self):
        return self.end_point

    def get_end_point_as_object(self):
        if self.end_point:
            end_x = self.end_point[0]
            end_y = self.end_point[1]

            return self.locations[end_y][end_x]
        else:
            return None

    def reset(self):
        for row in self.locations:
            for location in row:
                if not location.is_wall():
                    location.reset_location()
        self.start_point = None
        self.end_point = None

    def reset_walls(self):
        for row in self.locations:
            for location in row:
                if location.is_wall():
                    location.reset_location()

    def get_point_as_object(self, x, y):
        return self.locations[y][x]


class ButtonContainer(Frame):
    def __init__(self, master):
        super(ButtonContainer, self).__init__(master, relief=FLAT)

        self.button_manager = None


        self.start_point_button = Button(master=self,
                                         text="Start Point",
                                         bg="white",
                                         fg="black",
                                         relief="raised",
                                         command=self.start_point_button_clicked)
        self.start_point_button.pack()

        self.end_point_button = Button(master=self,
                                       text="End Point",
                                       bg="white",
                                       fg="black",
                                       relief="raised",
                                       command=self.end_point_button_clicked)
        self.end_point_button.pack()

        self.reset_button = Button(master=self,
                                   text="Reset",
                                   bg="white",
                                   fg="black",
                                   relief="raised",
                                   command=self.reset_clicked)
        self.reset_button.pack()

        self.reset_walls_button = Button(master=self,
                                         text="Reset Walls",
                                         bg="white",
                                         fg="black",
                                         relief="raised",
                                         command=self.reset_walls_clicked)
        self.reset_walls_button.pack()

        self.A_star_button = Button(master=self,
                                    text="A* Search",
                                    bg="white",
                                    fg="black",
                                    relief="raised",
                                    command=self.A_star_button_clicked)
        self.A_star_button.pack()


    def start_point_button_clicked(self):
        self.button_manager.start_point_button_clicked()

    def end_point_button_clicked(self):
        self.button_manager.end_point_button_clicked()

    def reset_clicked(self):
        self.button_manager.reset_clicked()

    def reset_walls_clicked(self):
        self.button_manager.reset_walls_clicked()

    def A_star_button_clicked(self):
        self.button_manager.A_star_button_clicked()


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

    def bind_end_point_setting(self):
        for row in self.grid.locations:
            for location in row:
                location.bind("<Button-1>", self.end_location_clicked)

    def end_location_clicked(self, event):
        self.grid.set_end_event_handler(event)
        self.bind_wall_setting()


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

    def reset_clicked(self):
        self.window.grid.reset()

    def reset_walls_clicked(self):
        self.window.grid.reset_walls()

    def A_star_button_clicked(self):
        if self.window.grid.get_start_point_as_pair() and self.window.grid.get_end_point_as_pair():
            A_star_searcher = AStarSearch(self.window.grid, self.window)
            A_star_searcher.search()
