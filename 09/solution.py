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
                        highest_section_int = None
                        highest_section = None
                        for object in objects:
                            if isinstance(object, Section):
                                if (highest_section_int == None) or (object.index > highest_section_int):
                                    highest_section_int = object.index
                                    highest_section = repr(object)
                        if highest_section == None:
                            char = '#'
                        else:
                            char = highest_section
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


# Section represents a section of a rope
class Section(Point):

    objects = []

    def __init__(self, x, y):
        super().__init__(x, y)

        # `leader` is the next rope section ahead
        # `follower` is the next rope section behind
        # `index` is the count of other rope sections ahead of this instance
        if Section.objects:
            self.leader = Section.objects[-1]
            self.follower = None
            self.leader.follower = self
            
            self.index = len(Section.objects)

        else:
            self.leader = None
            self.index = 0

        Section.objects.append(self)

    def __str__(self):
        return "Section {} at {}".format(self.index, super().__str__())

    # For displaying in a grid
    def __repr__(self):
        return "{}".format(self.index)


# Visit represents a position that the rope has visited
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
        return "#"


Visit(-1,0)
Visit(0,0)
Visit(1,0)
Visit(2,0)
Visit(3,0)
Visit(4,0)
Section(1,-1)
Section(1,-1)
Section(0,0)
Section(1,1)
Section(2,1)
Section(3,1)

Point.print_grid()
