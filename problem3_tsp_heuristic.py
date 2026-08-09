"""
CSC2103 - Travelling Salesman Problem (TSP) using the Nearest Neighbour Heuristic

Notes
- Each location is restricted to its 3 NEAREST NEIGHBOURS
- The heuristic is run starting from a location chosen by the user, and at each
  step the user can pick from the nearest unvisited candidates (or take the
  default = nearest option).
- Distances (in km) between every pair of locations were looked up directly via
  Google Maps and entered below.

algo reference: https://www.youtube.com/watch?v=ojjnd5gEMuk

git status# Updated on 04-08-2026

"""

destinations = [
    "Sunway University",
    "Sunway Pyramid",
    "Sunway Square",
    "Sunway Medical Centre",
    "Sunway Geo",
]

abbreviations = [
     "University", 
     "Pyramid", 
     "Square", 
     "Medical Centre", 
     "Geo" 
]


# Order of cities: [Sunway University, Sunway Pyramid, Sunway Square, Sunway Medical Centre, Sunway Geo]
distance_matrix_km = [
    [0.00, 0.70, 0.55, 1.00, 1.80],  # Sunway University
    [0.70, 0.00, 1.40, 1.70, 2.20],  # Sunway Pyramid
    [0.55, 1.40, 0.00, 0.45, 1.30],  # Sunway Square
    [1.00, 1.70, 0.45, 0.00, 1.00],  # Sunway Medical Centre
    [1.80, 2.20, 1.30, 1.00, 0.00],  # Sunway Geo
]

d_nearest = 3

def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "="))
    print("=" * 60)


def print_matrix(destinations, distance_matrix_km):
    print("\n--- Distance Matrix in km ---")

    col_width = 20

    # Header row
    header = f"{'Location':<{col_width}}" + "".join(
        f"{name:<{col_width}}" for name in abbreviations
    )
    print(header)
    print("-" * len(header))

    # Matrix rows
    for i, row in enumerate(distance_matrix_km):
        row_str = f"{abbreviations[i]:<{col_width}}" + "".join(
            f"{dist:<{col_width}.2f}" for dist in row
        )
        print(row_str)

def get_k_nearest_neighbours(destinations, distance_matrix_km, k=d_nearest):
   # For every location, finds the 3 closest other locations.
    neighbours = {}
    for i in range(len(destinations)):
        candidates = [(j, distance_matrix_km[i][j]) for j in range(len(destinations)) if j != i]
        candidates.sort(key=lambda x: x[1])
        neighbours[i] = candidates[:k]
    return neighbours


def print_d_nearest(destinations, neighbours):
    print(f"\n--- {d_nearest} Nearest Neighbours per Location ---")
    for i, location in enumerate(destinations):
        pairs = [f"{destinations[j]} ({dist:.2f} km)" for j, dist in neighbours[i]]
        print(f"{location}:")
        for rank, pair in enumerate(pairs, start=1):
            print(f"   {rank}. {pair}")


def get_nearest_location(d_index, distance_matrix_km, neighbours, visited, k=d_nearest):

    candidates = [(j, dist) for j, dist in neighbours[d_index] if not visited[j]]

    if len(candidates) < k:
        seen = {j for j, _ in candidates}
        extra = [
            (j, distance_matrix_km[d_index][j])
            for j in range(len(distance_matrix_km))
            if not visited[j] and j != d_index and j not in seen
        ]
        extra.sort(key=lambda x: x[1])
        candidates += extra[: k - len(candidates)]

    candidates.sort(key=lambda x: x[1])
    return candidates


def interactive_nearest_neighbour_tsp(destinations, distance_matrix_km, neighbours, start_index):

    num_destinations = len(distance_matrix_km)
    visited = [False] * num_destinations
    tour = [start_index]
    visited[start_index] = True   #marks the starting location as visited

    current_location = start_index
    total_cost = 0.0
    step_details = []
    step_num = 1

    while len(tour) < num_destinations:
        candidates = get_nearest_location(current_location, distance_matrix_km, neighbours, visited)

        print(f"\n--- Step {step_num}: Currently at '{destinations[current_location]}' ---")
        print(f"{d_nearest} nearest unvisited location(s):")
        for idx, (candidate, dist) in enumerate(candidates, start=1):
            print(f"  {idx}. {destinations[candidate]:<25} ({dist:.2f} km away)")

        chosen = None
        default_choice = 1  # the nearest option, per the Nearest Neighbour heuristic
        while chosen is None:
            raw = input(
                f"Choose next location [1-{len(candidates)}] "
                f"(press Enter for nearest = option {default_choice}): "
            ).strip()
            if raw == "":
                chosen = default_choice
                break
            try:
                choice_num = int(raw)
                if 1 <= choice_num <= len(candidates):
                    chosen = choice_num
                else:
                    print(f"Please enter a number between 1 and {len(candidates)}.")
            except ValueError:
                print("Invalid input! Please enter a number.")

        next_location, dist = candidates[chosen - 1]
        was_top_choice = (chosen == 1)

        step_details.append((current_location, next_location, dist, was_top_choice))
        visited[next_location] = True
        tour.append(next_location)
        total_cost += dist
        current_location = next_location
        step_num += 1

        print(f"-> Travelling to '{destinations[next_location]}' ({dist:.2f} km)")

    # Return to the starting location to complete the cycle
    return_distance = distance_matrix_km[current_location][start_index]
    total_cost += return_distance
    tour.append(start_index)
    step_details.append((current_location, start_index, return_distance, True))
    print(f"\n--- Final Step: Return to starting location '{destinations[start_index]}' ({return_distance:.2f} km) ---")

    return tour, total_cost, step_details

#Summary of the tour
def print_step_details(destinations, step_details):
    print(f"{'From':<25} {'To':<25} {'Distance (km)':<14} {'Choice':<18}")
    print("-" * 82)
    for from_node, to_node, dist, was_nearest in step_details:
        note = "nearest option" if was_nearest else "user selected"
        print(f"{destinations[from_node]:<25} {destinations[to_node]:<25} {dist:<14.2f} {note:<18}")


def choose_starting_location(destinations):
    print("\n--- Select Starting Location ---")
    for idx, location in enumerate(destinations):
        print(f"{idx}: {location}")

    while True:
        try:
            start_idx = int(input(f"Enter start location index (0 to {len(destinations) - 1}): "))
            if 0 <= start_idx < len(destinations):
                return start_idx
            print("Please enter a value between 0 and 4.")
        except ValueError:
            print("Please enter a valid integer index.")


def run():
    print_header("Travelling Salesman Problem using Nearest Neighbour Heuristic")

    print_matrix(destinations, distance_matrix_km)

    neighbours = get_k_nearest_neighbours(destinations, distance_matrix_km, d_nearest)
    print_d_nearest(destinations, neighbours)

    start_index = choose_starting_location(destinations)

    print_header(f"STEP BY STEP TOUR FROM '{destinations[start_index].upper()}'")
    tour, total_cost, step_details = interactive_nearest_neighbour_tsp(
        destinations, distance_matrix_km, neighbours, start_index
    )

    print_header("SOLUTION & EXECUTION SUMMARY")
    print("\n--- Step-by-Step Traversal ---")
    print_step_details(destinations, step_details)

    route_names = " -> ".join([destinations[idx] for idx in tour])
    print("\n--- Final Route & Cost Summary ---")
    print(f"Full Tour   : {route_names}")
    print(f"Total Cost  : {total_cost:.2f} km")
    print("=" * 60)


if __name__ == "__main__":
    run()
