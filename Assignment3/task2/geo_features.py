from abc import ABC
from dataclasses import dataclass


@dataclass
class Location:
    Y: int = 0
    X: int = 0

    def __str__(self):
        return f"({self.Y},{self.X})"

    def deep_copy(self):
        return Location(self.Y, self.X)


@dataclass
class Size:
    height: int = 0
    width: int = 0


class GeoFeature(ABC):
    def __init__(self, location: Location, size: Size, type: str, name: str):
        self.location = location
        self.size = size
        self.type = type
        self.name = name


class Mountain(GeoFeature):
    def __init__(self, location: Location, size: Size, name: str, height: int):
        super().__init__(location, size, "mountain", name)
        self.height = height

    def __str__(self):
        return f"{self.type} {self.name}, height {self.height}"


class Lake(GeoFeature):
    def __init__(self, location: Location, size: Size, name: str, depth: int):
        super().__init__(location, size, "lake", name)
        self.depth = depth

    def __str__(self):
        return f"{self.type} {self.name}, depth {self.depth}"


class Crater(GeoFeature):
    def __init__(self, location: Location, size: Size, name: str, perimeter: int):
        super().__init__(location, size, "crater", name)
        self.perimeter = perimeter

    def __str__(self):
        return f"{self.type} {self.name}, perimeter {self.perimeter}"
