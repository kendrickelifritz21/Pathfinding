from tkinter import *


class Location(Frame):
    def __init__(self, master, x, y):
        super(Location, self).__init__(master, relief=SOLID, borderwidth=1, height=25, width=25, bg="white")
        self.wall = False
        self.coordinates = (x, y)
        self.neighbors = []

    def setWall(self):
        self.config(bg="#383b39")
        self.wall = True
        #print(self.coordinates)
        #print("neighbors: ", self.neighbors, "\n")

    def removeWall(self):
        self.config(bg="white")
        self.wall = False

    def isWall(self):
        return self.wall

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
        self.startPoint = None
        self.endPoint = None
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
        try:
            coordinates = widget.coordinates
            if coordinates != self.startPoint and coordinates != self.endPoint:
                widget.setWall()
        except AttributeError:
            pass

    def remove_wall(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            if coordinates != self.startPoint and coordinates != self.endPoint:
                widget.removeWall()
        except AttributeError:
            pass

    def buildGraph(self):
        for row in self.locations:
            for location in row:
                location.addNeighbors(self.width, self.height)

    def setStartPoint(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            self.startPoint = coordinates
            if widget.isWall():
                widget.removeWall()
            widget.config(bg="yellow")
        except AttributeError:
            pass

    def getStartPoint(self):
        return self.startPoint

    def setEndPoint(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            coordinates = widget.coordinates
            self.endPoint = coordinates
            if widget.isWall():
                widget.removeWall()
            widget.config(bg="green")
        except AttributeError:
            pass

    def getEndPoint(self):
        return self.endPoint

    def resetStartEnd(self):
        if self.startPoint:
            x, y = self.startPoint
            startLocation = self.locations[y][x]
            startLocation.config(bg="white")
            self.startPoint = None
        if self.endPoint:
            x, y = self.endPoint
            endLocation = self.locations[y][x]
            endLocation.config(bg="white")
            self.endPoint = None




class MyWindow(Tk):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.minsize(1350, 750)

        self.mazeGrid = LocationGrid(self, 50, 30)
        self.mazeGrid.pack(side=LEFT)

        self.buttonFrameContainer = Frame(master=self, relief=FLAT)
        self.buttonFrameContainer.pack(side=LEFT, fill=X, expand=True)

        self.button1 = Button(master=self.buttonFrameContainer, text="Start Point", bg="white")
        self.button1.bind("<Button-1>", self.startPointClicked)
        self.button1.pack()

        self.button2 = Button(master=self.buttonFrameContainer, text="End Point", bg="white")
        self.button2.bind("<Button-1>", self.endPointClicked)
        self.button2.pack()

        self.button3 = Button(master=self.buttonFrameContainer, text="Reset Start/End", bg="white")
        self.button3.bind("<Button-1>", self.resetStartEndClicked)
        self.button3.pack()

    def startPointClicked(self, event):
        if not self.mazeGrid.getStartPoint():
            self.unbindWallSetting()
            self.bindStartPointSetting()

    def endPointClicked(self, event):
        if not self.mazeGrid.getEndPoint():
            self.unbindWallSetting()
            self.bindEndPointSetting()

    def resetStartEndClicked(self, event):
        self.mazeGrid.resetStartEnd()

    def unbindWallSetting(self):
        for row in self.mazeGrid.locations:
            for location in row:
                location.unbind("<Button-1>")
                location.unbind("<Button-3>")
                location.unbind("<B1-Motion>")
                location.unbind("<B3-Motion>")

    def bindWallSetting(self):
        for row in self.mazeGrid.locations:
            for location in row:
                location.bind("<Button-1>", self.mazeGrid.left_click)
                location.bind("<Button-3>", self.mazeGrid.right_click)
                location.bind("<B1-Motion>", self.mazeGrid.left_moved)
                location.bind("<B3-Motion>", self.mazeGrid.right_moved)

    def bindStartPointSetting(self):
        for row in self.mazeGrid.locations:
            for location in row:
                location.bind("<Button-1>", self.setStartPoint)

    def setStartPoint(self, event):
        self.mazeGrid.setStartPoint(event)
        self.bindWallSetting()
        print(self.mazeGrid.getStartPoint())

    def bindEndPointSetting(self):
        for row in self.mazeGrid.locations:
            for location in row:
                location.bind("<Button-1>", self.setEndPoint)

    def setEndPoint(self, event):
        self.mazeGrid.setEndPoint(event)
        self.bindWallSetting()
        print(self.mazeGrid.getEndPoint())
