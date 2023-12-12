from typing import List, Optional


class Galaxy:
    objects = []
    field_height = 0
    field_width = 0

    def __init__(self, id: int, y: int, x: int) -> "Galaxy":
        self.id = id
        self.y = y
        self.x = x
        if self.find_galaxy_by_id(self.id) is None:
            self.generate_pairs()
            self.objects.append(self)
            self.update_field_size(self.y, self.x)
            print(f"{len(self.objects)}/428")

    def generate_pairs(self) -> None:
        for other in Galaxy.objects:
            GalaxyPair(other, self)

    @classmethod
    def find_galaxy_by_id(cls, id: int) -> Optional["Galaxy"]:
        for galaxy in cls.objects:
            if galaxy.id == id:
                return galaxy

    @classmethod
    def update_field_size(cls, y: int, x: int):
        if y > cls.field_height:
            cls.field_height = y
        if x > cls.field_width:
            cls.field_width = x

    @classmethod
    def find_galaxies_by_y(cls, y: int, gte: bool = False) -> List["Galaxy"]:
        matching_galaxies = []
        for galaxy in cls.objects:
            if galaxy.y == y or (gte and galaxy.y > y):
                matching_galaxies.append(galaxy)
        return matching_galaxies

    @classmethod
    def find_galaxies_by_x(cls, x: int, gte: bool = False) -> List["Galaxy"]:
        matching_galaxies = []
        for galaxy in cls.objects:
            if galaxy.x == x or (gte and galaxy.x > x):
                matching_galaxies.append(galaxy)
        return matching_galaxies

    @classmethod
    def expand_cosmos(cls, units: int) -> None:
        for y in range(cls.field_height - 1, -1, -1):
            galaxies_on_y = cls.find_galaxies_by_y(y)
            if len(galaxies_on_y) == 0:
                for galaxy in cls.find_galaxies_by_y(y, True):
                    galaxy.y += units
                Galaxy.field_height += units
        for x in range(cls.field_width - 1, -1, -1):
            galaxies_on_x = cls.find_galaxies_by_x(x)
            if len(galaxies_on_x) == 0:
                for galaxy in cls.find_galaxies_by_x(x, True):
                    galaxy.x += units
                Galaxy.field_width += units


class GalaxyPair:
    objects = []

    def __init__(self, first_galaxy: Galaxy, second_galaxy: Galaxy) -> "GalaxyPair":
        reverse = first_galaxy.id > second_galaxy.id
        self.first_galaxy = second_galaxy if reverse else first_galaxy
        self.second_galaxy = first_galaxy if reverse else second_galaxy
        if self.find_galaxy_pair(self.first_galaxy.id, self.second_galaxy.id) is None:
            self.objects.append(self)

    @property
    def distance(self) -> int:
        x_diff = self.first_galaxy.x - self.second_galaxy.x
        y_diff = self.first_galaxy.y - self.second_galaxy.y
        return abs(x_diff) + abs(y_diff)

    @classmethod
    def find_galaxy_pair(cls, first_id: int, second_id: int) -> Optional["GalaxyPair"]:
        for pair in cls.objects:
            if pair.first_galaxy.id == first_id and pair.second_galaxy.id == second_id:
                return pair


def parse_input(lines: List[str]):
    index = 0
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            content = line[x]
            if content == "#":
                Galaxy(index, y, x)
                index += 1


with open("2023/11/input.txt") as input:
    lines = input.readlines()
parse_input(lines)

# Solve part 1
Galaxy.expand_cosmos(1) # 1 + 1 = 2
distance_sum = 0
for pair in GalaxyPair.objects:
    distance_sum += pair.distance
print("Solution for part 1: {}".format(distance_sum))

# Solve part 2
Galaxy.expand_cosmos(499999) # 2 + 499999 + 499999 = 1000000
distance_sum = 0
for pair in GalaxyPair.objects:
    distance_sum += pair.distance
print("Solution for part 2: {}".format(distance_sum))
