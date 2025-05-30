import robot
import geo_features

if __name__ == "__main__":
    features_map = geo_features.GeoMap()

    # read the file
    with open("./Assignment3/task1/geo_features.txt", "r") as file:
        X = 0
        Y = 0
        for line in file:
            # split the line into parts
            tokens = line.strip().split(",")
            if len(tokens) < 3:
                X = int(tokens[1])
                Y = int(tokens[0])
                features_map = geo_features.GeoMap(X, Y)
            else:
                location = geo_features.Location(int(tokens[0]), int(tokens[1]))
                size = geo_features.Size(0, 0)
                name = tokens[3]
                if tokens[2] == "mountain":
                    height = int(tokens[4])
                    feature = geo_features.Mountain(location, size, name, height)
                elif tokens[2] == "lake":
                    depth = int(tokens[4])
                    feature = geo_features.Lake(location, size, name, depth)
                elif tokens[2] == "crater":
                    perimeter = int(tokens[4])
                    feature = geo_features.Crater(location, size, name, perimeter)
                else:
                    continue
                features_map.add_feature(feature)

    robbie = robot.Robot()

    command = ""
    while command != "quit":
        command = input("> ")
        if command == "show map":
            for j in range(Y):
                line = ""
                for i in range(X):
                    feature = features_map.get_feature(geo_features.Location(j, i))
                    if feature is not None:
                        line += feature.type[0]
                    else:
                        line += "."
                print(line)

        elif command.startswith("info"):
            tokens = command.split(" ")
            if (
                int(tokens[1]) >= 0
                and int(tokens[1]) < Y
                and int(tokens[2]) >= 0
                and int(tokens[2]) < X
            ):
                feature = features_map.get_feature(
                    geo_features.Location(int(tokens[2]), int(tokens[1]))
                )
                if feature is not None:
                    print(str(feature))
                else:
                    print("no information found")

        elif command.startswith("moveto"):
            tokens = command.split(" ")
            destX = int(tokens[1])
            destY = int(tokens[2])
            robbie.move(geo_features.Location(destX, destY), features_map)

        elif command.startswith("explore"):
            robbie.explore(features_map)

        elif command.startswith("mission"):
            tokens = command[8:].split(",")
            dest_list = []
            for token in tokens:
                token = token.strip()
                if token in features_map.get_features():
                    dest_list.append(features_map.get_features()[token])

            robbie.missions(dest_list, features_map)

        elif command == "display journey":
            robbie.display_journey()

    print("goodbye")
