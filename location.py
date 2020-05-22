from tkinter import *


class Location(Frame):
    def __init__(self, master, x, y):
        super(Location, self).__init__(master, relief=SOLID, borderwidth=1, height=25, width=25, bg="white")
        self.wall = False
        self.coordinates = (x, y)
        self.neighbors = []

    def setWall(self):
        self.config(bg="green")
        self.wall = True
        print(self.coordinates)
        print("neighbors: ", self.neighbors, "\n")

    def removeWall(self):
        self.config(bg="white")
        self.wall = False

    def addNeighbors(self, width, height):
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

                location.bind("<Button-1>", self.left_click)
                location.bind("<Button-3>", self.right_click)
                location.bind("<B1-Motion>", self.left_moved)
                location.bind("<B3-Motion>", self.right_moved)

                locations[y].append(location)

        self.locations = locations
        self.left_pressed = False
        self.right_pressed = False

        self.buildGraph()

    def left_click(self, event):
        self.left_pressed = True
        self.set_wall(event)

    def release_left(self, event):
        self.left_pressed = False

    def left_moved(self, event):
        self.set_wall(event)

    def right_click(self, event):
        self.right_pressed = True
        self.remove_wall(event)

    def release_right(self, event):
        self.right_pressed = False

    def right_moved(self, event):
        self.remove_wall(event)

    def set_wall(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        widget.setWall()

    def remove_wall(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        widget.removeWall()

    def buildGraph(self):
        for row in self.locations:
            for location in row:
                location.addNeighbors(self.width, self.height)


class MyWindow(Tk):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.minsize(1350, 750)

        mazeGrid = LocationGrid(self, 50, 30)
        mazeGrid.pack(side=LEFT)

        buttonFrameContainer = Frame(master=self, relief=FLAT)
        buttonFrameContainer.pack(side=LEFT, fill=X, expand=True)

        button1 = Button(master=buttonFrameContainer, text="Start Point", bg="white")
        button1.pack()

        button2 = Button(master=buttonFrameContainer, text="asdf", bg="white")
        button2.pack()

        button3 = Button(master=buttonFrameContainer, text="123", bg="white")
        button3.pack()