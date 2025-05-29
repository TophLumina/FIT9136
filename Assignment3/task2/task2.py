import robot
import geo_features

if __name__ == "__main__":
    features = []

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
                features = [[None] * X for _ in range(Y)]
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
                features[location.Y][location.X] = feature

    robbie = robot.Robot()

    command = ""
    while command != "quit":
        command = input("> ")
        if command == "show map":
            for j in range(Y):
                line = ""
                for i in range(X):
                    feature = features[j][i]
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
                feature = features[int(tokens[1])][int(tokens[2])]
                if feature is not None:
                    print(str(feature))
                else:
                    print("no information found")

        elif command.startswith("moveto"):
            tokens = command.split(" ")
            destX = int(tokens[1])
            destY = int(tokens[2])
            robbie.move(geo_features.Location(destX, destY), X, Y)

        elif command.startswith("explore"):
            robbie.explore(features)

        elif command == "display journey":
            robbie.display_journey()

    print("goodbye")
