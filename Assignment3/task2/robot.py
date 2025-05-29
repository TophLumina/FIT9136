import geo_features
import math

class JourneyItem:
    def __init__(self, duration: list[int], log: tuple[str, list]):
        self.duration = duration
        self.log = log

    def __str__(self):
        string = f"Day "
        if self.duration[0] + 1 == self.duration[1]:
            string += f"{self.duration[1]}: "
        else:
            string += f"{self.duration[0] + 1}-{self.duration[1]}: "
        if self.log[0] == "move":
            string += "move "
            for loc in self.log[1]:
                string += f"{loc} -> "
            string = string[:-4]
        if self.log[0] == "explore":
            string += "explore "
            for des in self.log[1]:
                string += des + " "
        string = string[:-1]
        return string


class ExplorationSpec:
    Mountain: int = 6
    Lake: int = 8
    Crater: int = 10
    MountainExplored: bool = False
    LakeExplored: bool = False
    CraterExplored: bool = False


class Robot:
    def __init__(self):
        self.explore_spec = ExplorationSpec()
        self.location = geo_features.Location()
        self.journey = []
        self.days = 0

    def step(self, dest: geo_features.Location, journey_item: JourneyItem, boundaryX: int, boundaryY: int) -> None:
        if self.location.X != dest.X:
            # need to warp across the boundary
            if abs(dest.X - self.location.X) >= boundaryX / 2:
                self.location.X = (self.location.X + (1 if dest.X < self.location.X else -1)) % boundaryX
            else:
                self.location.X = (self.location.X + (1 if dest.X > self.location.X else -1)) % boundaryX
            journey_item.duration = [journey_item.duration[0], journey_item.duration[1] + 1]
            journey_item.log[1].append(geo_features.Location(self.location.Y, self.location.X))
            return
        
        if self.location.Y != dest.Y:
            # need to warp across the boundary
            if abs(dest.Y - self.location.Y) >= boundaryY / 2:
                self.location.Y = (self.location.Y + (1 if dest.Y < self.location.Y else -1)) % boundaryY
            else:
                self.location.Y = (self.location.Y + (1 if dest.Y > self.location.Y else -1)) % boundaryY
            journey_item.duration = [journey_item.duration[0], journey_item.duration[1] + 1]
            journey_item.log[1].append(geo_features.Location(self.location.Y, self.location.X))
            return

    def move(self, dest: geo_features.Location, boundaryX: int, boundaryY: int) -> None:
        if dest.X < 0 or dest.X >= boundaryX or dest.Y < 0 or dest.Y >= boundaryY:
            raise ValueError("Destination out of bounds")
        
        if self.location == dest:
            print("same location")
            return
        
        print(f"move from {self.location} to {dest}")
        journey_item = JourneyItem((self.days, self.days), ("move", [self.location.deep_copy()]))
        while self.location != dest:
            self.step(dest, journey_item, boundaryX, boundaryY)
            self.days += 1
        self.journey.append(journey_item)

    def explore(self, map: list[list[geo_features.GeoFeature]]) -> None:
        feature = map[self.location.Y][self.location.X]
        if feature is None:
            print("nothing to explore")
            return
        print(f"explore {feature.type} {feature.name}")
        
        if feature.type == "mountain":
            if self.explore_spec.MountainExplored:
                self.explore_spec.Mountain *= 1.2
            days_cost = math.ceil(feature.height / self.explore_spec.Mountain)
            self.explore_spec.MountainExplored = True
        elif feature.type == "lake":
            if self.explore_spec.LakeExplored:
                self.explore_spec.Lake *= 1.2
            days_cost = math.ceil(feature.depth / self.explore_spec.Lake)
            self.explore_spec.LakeExplored = True
        elif feature.type == "crater":
            if self.explore_spec.CraterExplored:
                self.explore_spec.Crater *= 1.2
            days_cost = math.ceil(feature.perimeter / self.explore_spec.Crater)
            self.explore_spec.CraterExplored = True

        journey_item = JourneyItem((self.days, self.days + days_cost), ("explore", [feature.type, feature.name]))
        self.journey.append(journey_item)
        self.days += days_cost

    def display_journey(self) -> None:
        if len(self.journey) == 0:
            print("")
            return
        for item in self.journey:
            print(str(item))
