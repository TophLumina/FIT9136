# Please enter your code for importing math functions to be used
x = [10.1, 0.4, 6.9, 4.2, 14.1, 15.9]
y = [17.7, 3.1, 9.0, 2.7, 41.5, 33.3]
cities = ["Elabro", "Nutunyu", "Barimba", "Duduth", "Tromsu", "Pranho"]
# Please enter your code here for finding the pair of cities with the shortest distance.
# Please enter your code here for displaying the pair of cities with the shortest distance.

cities_dist2 = {
    (cities[u], cities[v]): (x[u] - x[v]) ** 2 + (y[u] - y[v]) ** 2
    for u in range(len(cities) - 1)
    for v in range(1, len(cities))
    if v > u
}

min_names = list(cities_dist2.keys())[0]
min_dist = cities_dist2[min_names]
for k, v in cities_dist2.items():
    if v < min_dist:
        min_names = k
        min_dist = v

print(
    "The two cities that are closest to each other are:",
    min_names[0],
    "and",
    min_names[1],
)
