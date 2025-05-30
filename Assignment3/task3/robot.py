from abc import ABC
from dataclasses import dataclass
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
        string = string.strip()
        return string


@dataclass
class ExplorationExperience:
    MountainExplored: int = 0
    LakeExplored: int = 0
    CraterExplored: int = 0


@dataclass
class ExplorationSpec(ABC):
    pass


@dataclass
class RoboticExplorationSpec(ExplorationSpec):
    name = "robot"
    Mountain: int = 6
    Lake: int = 8
    Crater: int = 10


@dataclass
class DroneExplorationSpec(ExplorationSpec):
    name = "drone"
    Mountain: int = 12
    Lake: int = 6
    Crater: int = 8


@dataclass
class AUVExplorationSpec(ExplorationSpec):
    name = "AUV"
    Mountain: int = 2
    Lake: int = 12
    Crater: int = 6


class Robot:
    def __init__(self):
        self.experience = ExplorationExperience()
        self.explore_specs = {
            "robotic": RoboticExplorationSpec(),
            "drone": DroneExplorationSpec(),
            "AUV": AUVExplorationSpec(),
        }
        self.explore_spec = self.explore_specs[
            "robotic"
        ]  # default to robotic exploration
        self.location = geo_features.Location()
        self.journey = []
        self.days = 0

    def step(
        self,
        dest: geo_features.Location,
        journey_item: JourneyItem,
        map: geo_features.GeoMap,
    ) -> None:
        if self.location.X != dest.X:
            # need to warp across the boundary
            if abs(dest.X - self.location.X) >= map.BoundaryX / 2:
                self.location.X = (
                    self.location.X + (1 if dest.X < self.location.X else -1)
                ) % map.BoundaryX
            else:
                self.location.X = (
                    self.location.X + (1 if dest.X > self.location.X else -1)
                ) % map.BoundaryX
            journey_item.duration = [
                journey_item.duration[0],
                journey_item.duration[1] + 1,
            ]
            journey_item.log[1].append(
                geo_features.Location(self.location.Y, self.location.X)
            )
            return

        if self.location.Y != dest.Y:
            # need to warp across the boundary
            if abs(dest.Y - self.location.Y) >= map.BoundaryY / 2:
                self.location.Y = (
                    self.location.Y + (1 if dest.Y < self.location.Y else -1)
                ) % map.BoundaryY
            else:
                self.location.Y = (
                    self.location.Y + (1 if dest.Y > self.location.Y else -1)
                ) % map.BoundaryY
            journey_item.duration = [
                journey_item.duration[0],
                journey_item.duration[1] + 1,
            ]
            journey_item.log[1].append(
                geo_features.Location(self.location.Y, self.location.X)
            )
            return

    def move(
        self,
        dest: geo_features.Location,
        map: geo_features.GeoMap,
        need_explore: bool = False,
    ) -> None:
        if (
            dest.X < 0
            or dest.X >= map.BoundaryX
            or dest.Y < 0
            or dest.Y >= map.BoundaryY
        ):
            raise ValueError("Destination out of bounds")

        if self.location == dest:
            print("same location", end=", " if need_explore else "\n")
            return

        print(
            f"move from {self.location} to {dest}",
            end=" then " if need_explore else "\n",
        )
        journey_item = JourneyItem(
            (self.days, self.days), ("move", [self.location.deep_copy()])
        )
        while self.location != dest:
            self.step(dest, journey_item, map)
            self.days += 1
        self.journey.append(journey_item)

    def explore(self, map: geo_features.GeoMap) -> None:
        feature = map.get_feature(self.location)
        if feature is None:
            print("nothing to explore")
            return
        print(f"explore {feature.type} {feature.name}")

        if feature.type == "mountain":
            days_cost = math.ceil(
                feature.height
                / (
                    self.explore_spec.Mountain
                    * pow(1.2, self.experience.MountainExplored)
                )
            )
            self.experience.MountainExplored += 1
        elif feature.type == "lake":
            days_cost = math.ceil(
                feature.depth
                / (self.explore_spec.Lake * pow(1.2, self.experience.LakeExplored))
            )
            self.experience.LakeExplored += 1
        elif feature.type == "crater":
            days_cost = math.ceil(
                feature.perimeter
                / (self.explore_spec.Crater * pow(1.2, self.experience.CraterExplored))
            )
            self.experience.CraterExplored += 1

        journey_item = JourneyItem(
            (self.days, self.days + days_cost),
            ("explore", [feature.type, feature.name]),
        )
        self.journey.append(journey_item)
        self.days += days_cost

    def transform(self, spec_str: str) -> None:
        if spec_str not in self.explore_specs:
            raise ValueError(f"Unknown exploration spec: {spec_str}")
        if self.explore_spec.name == self.explore_specs[spec_str].name:
            print("no transformation")
            return
        self.explore_spec = self.explore_specs[spec_str]
        print(
            f"transform into "
            + ("an " if spec_str == "AUV" else "a ")
            + self.explore_spec.name
        )

    def transform_to_default(self) -> None:
        self.explore_spec = self.explore_specs["robotic"]

    def mission(self, dest: geo_features.GeoFeature, map: geo_features.GeoMap) -> None:
        self.move(dest.location, map, True)
        self.explore(map)

    def missions(
        self, dest_list: list[geo_features.GeoFeature], map: geo_features.GeoMap
    ) -> None:
        cost_robotic = 0
        cost_drone = 0
        cost_auv = 0
        for dest in dest_list:
            if dest.type == "mountain":
                speed_robotic = self.explore_specs["robotic"].Mountain
                speed_drone = self.explore_specs["drone"].Mountain
                speed_auv = self.explore_specs["AUV"].Mountain
                cost_robotic += math.ceil(
                    dest.height
                    / (speed_robotic * (pow(1.2, self.experience.MountainExplored)))
                )
                cost_drone += math.ceil(
                    dest.height
                    / (speed_drone * pow(1.2, self.experience.MountainExplored))
                )
                cost_auv += math.ceil(
                    dest.height
                    / (speed_auv * pow(1.2, self.experience.MountainExplored))
                )
            elif dest.type == "lake":
                speed_robotic = self.explore_specs["robotic"].Lake
                speed_drone = self.explore_specs["drone"].Lake
                speed_auv = self.explore_specs["AUV"].Lake
                cost_robotic += math.ceil(
                    dest.depth
                    / (speed_robotic * pow(1.2, self.experience.LakeExplored))
                )
                cost_drone += math.ceil(
                    dest.depth / (speed_drone * pow(1.2, self.experience.LakeExplored))
                )
                cost_auv += math.ceil(
                    dest.depth / (speed_auv * pow(1.2, self.experience.LakeExplored))
                )
            elif dest.type == "crater":
                speed_robotic = self.explore_specs["robotic"].Crater
                speed_drone = self.explore_specs["drone"].Crater
                speed_auv = self.explore_specs["AUV"].Crater
                cost_robotic += math.ceil(
                    dest.perimeter
                    / (speed_robotic * pow(1.2, self.experience.CraterExplored))
                )
                cost_drone += math.ceil(
                    dest.perimeter
                    / (speed_drone * pow(1.2, self.experience.CraterExplored))
                )
                cost_auv += math.ceil(
                    dest.perimeter
                    / (speed_auv * pow(1.2, self.experience.CraterExplored))
                )

        # Determine the best transformation option
        min_cost = cost_auv
        best_spec = "AUV"

        if cost_drone <= min_cost:
            min_cost = cost_drone
            best_spec = "drone"

        if cost_robotic <= min_cost:
            min_cost = cost_robotic
            best_spec = "robotic"

        self.transform(best_spec)

        for dest in dest_list:
            self.mission(dest, map)

        self.transform_to_default()  # reset to default after each mission

    def display_journey(self) -> None:
        if len(self.journey) == 0:
            print("")
            return
        for item in self.journey:
            print(str(item))
