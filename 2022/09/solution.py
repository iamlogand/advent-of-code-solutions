import os, re, time


# Point represents a thing at a specific position on a two dimensional plane
class Point():

    objects = set()

    # Remove an object
    def remove_object(x, y, type):
        objects = list(Visit.get_objects(x, y, type))
        if objects:
            Point.objects.remove(objects[0])

    # Get object by coordinates
    @classmethod
    def get_objects(cls, x, y, type=None):
        objects = set()
        for object in cls.objects:
            if object.x == x and object.y == y:
                if type == None or isinstance(object, type):
                    objects.add(object)
        return objects

    # Get max distance of instances from the origin in four directions:
    # up, left, down, right
    def get_bounds():
        u_max = l_max = d_max = r_max = 0
        for object in Point.objects:
            x = object.x
            y = object.y

            if x < l_max:
                l_max = x
            elif x > r_max:
                r_max = x
            
            if y < u_max:
                u_max = y
            elif y > d_max:
                d_max = y
        return u_max, l_max, d_max, r_max

    # Print a grid of Points
    def print_grid():
        u_max, l_max, d_max, r_max = Point.get_bounds()
        for y in range(u_max, d_max + 1):
            for x in range(l_max, r_max + 1):
                objects = Point.get_objects(x, y)
                if objects:
                    if len(objects) == 1:
                        char = repr(list(objects)[0])
                    else:
                        highest_knot_int = None
                        highest_knot = None
                        for object in objects:
                            if isinstance(object, Knot):
                                if (highest_knot_int == None) or (object.index > highest_knot_int):
                                    highest_knot_int = object.index
                                    highest_knot = repr(object)
                        if highest_knot == None:
                            char = '#'
                        else:
                            char = highest_knot
                else:
                    char = "."
                print(char, end=" ")
            print()

    def __init__(self, x, y):

        # Position is represented by integer x-y coordinates
        self.x = x
        self.y = y

        Point.objects.add(self)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


# knot represents a knot of a rope
class Knot(Point):

    objects = []

    def __init__(self, x, y):
        super().__init__(x, y)

        # `leader` is the next rope knot ahead
        # `follower` is the next rope knot behind
        # `index` is the count of other rope knots ahead of this instance
        if Knot.objects:
            self.leader = Knot.objects[-1]
            self.follower = None
            self.leader.follower = self
            self.index = len(Knot.objects)
        else:
            self.leader = None
            self.index = 0

        Knot.objects.append(self)

        # Visit starting position
        Visit(self.x, self.y)

    def __str__(self):
        return "knot {} at {}".format(self.index, super().__str__())

    # For displaying in a grid - this is very handy for testing and debugging
    def __repr__(self):
        return "\033[1;31;40m{}\033[0m".format(self.index)

    # Move based on a command (only possible for head knot)
    def command_move(self, command):
        if self.index == 0:

            old_x = self.x
            old_y = self.y

            match command:
                case "U":
                    self.y = self.y - 1
                case "L":
                    self.x = self.x - 1
                case "D":
                    self.y = self.y + 1
                case "R":
                    self.x = self.x + 1
                case _:
                    # Raise exception if command is invalid
                    raise Exception("Invalid command")

            # Drag follower
            if self.follower:
                self.follower.drag(self.x, self.y, old_x, old_y, self.x - old_x, self.y - old_y, False)
        
        else:
            # Raise exception if not the head knot
            raise Exception("Only the head knot of the rope can be moved based on a command")

    # Move by being dragged by leader
    def drag(self, leader_new_x, leader_new_y, leader_old_x, leader_old_y, head_delta_x, head_delta_y, diagonal):
        x_space = abs(self.x - leader_new_x)
        y_space = abs(self.y - leader_new_y)

        # Determine if movement is needed
        if x_space > 1 or y_space > 1:

            old_x = self.x
            old_y = self.y

            # Move up
            if leader_new_y < self.y:
                self.y -= 1
            # Move left
            if leader_new_x < self.x:
                self.x -= 1
            # Move down
            if leader_new_y > self.y:
                self.y += 1
            # Move right
            if leader_new_x > self.x:
                self.x += 1

            # Drag follower
            if self.follower:
                self.follower.drag(self.x, self.y, old_x, old_y, head_delta_x, head_delta_y, diagonal)
            else:
                Visit(self.x, self.y)


# Visit represents a position that the tail of the rope has visited
class Visit(Point):

    objects = set()

    # Remove an object
    def remove_object(x, y):
        Point.remove_object(x, y, Visit)  # Execute superclass method

        visits = list(Visit.get_objects(x, y))
        if visits:
            Visit.objects.remove(visits[0])

    def __init__(self, x, y):
        super().__init__(x, y)

        # Remove any other Visit instance at the same position, so
        # there can only ever be one Visit instance at any one position
        Visit.remove_object(x, y)

        Visit.objects.add(self)

    def __str__(self):
        return "Visit at {}".format(super().__str__())

    # For displaying in a grid
    def __repr__(self):
        return '\033[1;33;40m#\033[0m'


# Create rope
number_of_knots = 10
for knot in range(number_of_knots):
    Knot(0,0)

with open('09/input.txt') as file:
    lines = file.readlines()

# Issue command movements
for line in lines:
    elements = re.split(" ", line)

    command = elements[0]
    multiplier = int(elements[1])

    for i in range(multiplier):
        Knot.objects[0].command_move(command)

        # UNCOMMENT THIS TO SEE A RENDER OF THE GRID
        time.sleep(0.1)
        os.system("cls")
        Point.print_grid()

# Count visits
visit_count = len(Visit.objects)
print("\nPositions visited by tail: {}".format(visit_count))