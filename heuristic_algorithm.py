"""
CSC2103 - Travelling Salesman Problem (TSP) using the Nearest Neighbour Heuristic
Real-life dataset: 5 landmarks in Bandar Sunway, Selangor, Malaysia.

Notes
- Each location is restricted to its 3 NEAREST NEIGHBOURS (as instructed by the
  lecturer), instead of considering every other location. This mirrors how the
  heuristic is used in practice for larger, real-world graphs where computing/
  storing a full distance matrix is expensive - each node only "knows" about a
  handful of its closest candidates.
- The heuristic is run starting from EVERY location, and the cheapest resulting
  tour is reported as the BEST ROUTE (Nearest Neighbour is a heuristic, so the
  quality of the result depends heavily on the starting point).
- Distances are derived from real GPS coordinates (verified against Google Maps
  Places data for each landmark), converted from straight-line distance to an
  estimated walking/road distance using a 1.3x correction factor (Bandar Sunway
  locations are connected via elevated walkways and roads, not straight lines).

algo reference: https://www.youtube.com/watch?v=ojjnd5gEMuk
"""

import math

# Real GPS coordinates (latitude, longitude), verified via Google Maps
COORDINATES = {
    "Sunway University": (3.0672267, 101.6038410),
    "Sunway Pyramid": (3.0731724, 101.6075559),
    "Sunway Square": (3.0651060, 101.6050867),
    "Sunway Medical Centre": (3.0658578, 101.6094760),
    "Sunway Geo": (3.0648330, 101.6089520),
}

# Correction factor to convert straight-line ("as the crow flies") distance
# into a rough estimate of real walking/road distance in Bandar Sunway
ROAD_FACTOR = 1.3

# Number of nearest neighbours each location is allowed to consider
K_NEAREST = 3


def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "="))
    print("=" * 60)


def haversine_distance(coord1, coord2):
    """Great-circle distance between two (lat, lon) points, in metres."""
    R = 6371000  # Earth radius in metres
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def build_distance_matrix(cities, coordinates):
    """Builds a real, GPS-derived distance matrix (in metres)."""
    n = len(cities)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                straight_line = haversine_distance(coordinates[cities[i]], coordinates[cities[j]])
                matrix[i][j] = round(straight_line * ROAD_FACTOR, 1)
    return matrix


def print_matrix(cities, matrix):
    """Displays the distance matrix as a formatted table."""
    print("\n--- Distance Matrix (metres, GPS-derived) ---")
    header = f"{'':<24}" + "".join([f"{city[:14]:<16}" for city in cities])
    print(header)
    print("-" * len(header))

    for i, row in enumerate(matrix):
        row_str = f"{cities[i]:<24}" + "".join([f"{dist:<16.1f}" for dist in row])
        print(row_str)


def get_k_nearest_neighbours(cities, matrix, k=K_NEAREST):
    """
    For every location, finds the k closest OTHER locations.
    Returns a dict: {city_index: [(neighbour_index, distance), ...]} sorted by distance.
    """
    neighbours = {}
    for i in range(len(cities)):
        candidates = [(j, matrix[i][j]) for j in range(len(cities)) if j != i]
        candidates.sort(key=lambda x: x[1])
        neighbours[i] = candidates[:k]
    return neighbours


def print_k_nearest(cities, neighbours):
    print(f"\n--- {K_NEAREST} Nearest Neighbours per Location ---")
    for i, city in enumerate(cities):
        pairs = [f"{cities[j]} ({dist:.1f} m)" for j, dist in neighbours[i]]
        print(f"{city}:")
        for rank, pair in enumerate(pairs, start=1):
            print(f"   {rank}. {pair}")


def nearest_neighbour_tsp(distance_matrix, neighbours, start_index=0):
    """
    Solves TSP using the Nearest Neighbour Heuristic, restricted to each
    location's k-nearest-neighbour candidate list.

    If all k candidates for the current location have already been visited,
    falls back to searching the full distance matrix for the closest
    unvisited location (so the algorithm can still always complete a tour).

    Time Complexity: O(V^2) worst case (fallback search), O(V*k) typical
    Space Complexity: O(V)
    """
    num_cities = len(distance_matrix)
    visited = [False] * num_cities
    tour = [start_index]
    visited[start_index] = True

    current_city = start_index
    total_cost = 0
    step_details = []

    for _ in range(num_cities - 1):
        nearest_city = None
        min_distance = float('inf')
        via_fallback = False

        # 1. First, try the current city's k-nearest-neighbour candidate list
        for candidate, dist in neighbours[current_city]:
            if not visited[candidate] and dist < min_distance:
                min_distance = dist
                nearest_city = candidate

        # 2. Fallback: if none of the k candidates are available, search all cities
        if nearest_city is None:
            for next_city in range(num_cities):
                if not visited[next_city] and distance_matrix[current_city][next_city] < min_distance:
                    min_distance = distance_matrix[current_city][next_city]
                    nearest_city = next_city
            via_fallback = True

        step_details.append((current_city, nearest_city, min_distance, via_fallback))

        visited[nearest_city] = True
        tour.append(nearest_city)
        total_cost += min_distance
        current_city = nearest_city

    # Return to the starting city to complete the cycle
    return_distance = distance_matrix[current_city][start_index]
    total_cost += return_distance
    tour.append(start_index)
    step_details.append((current_city, start_index, return_distance, False))

    return tour, total_cost, step_details


def find_best_route(cities, distance_matrix, neighbours):
    """Runs the heuristic from every possible starting location and keeps the cheapest tour."""
    best_result = None
    all_results = []

    for start_index in range(len(cities)):
        tour, cost, steps = nearest_neighbour_tsp(distance_matrix, neighbours, start_index)
        all_results.append((start_index, tour, cost, steps))
        if best_result is None or cost < best_result[2]:
            best_result = (start_index, tour, cost, steps)

    return best_result, all_results


def print_step_details(cities, step_details):
    print(f"{'From':<25} {'To':<25} {'Distance (m)':<14} {'Note':<24}")
    print("-" * 88)
    for from_node, to_node, dist, fallback in step_details:
        note = "outside top-3 (fallback)" if fallback else "top-3 neighbour"
        print(f"{cities[from_node]:<25} {cities[to_node]:<25} {dist:<14.1f} {note:<24}")


def main():
    print_header("CSC2103: TSP NEAREST NEIGHBOUR HEURISTIC")
    print("Real-life dataset: 5 landmarks in Bandar Sunway, Selangor, Malaysia")
    print("(coordinates verified via Google Maps)")

    cities = list(COORDINATES.keys())
    matrix = build_distance_matrix(cities, COORDINATES)

    print_matrix(cities, matrix)

    neighbours = get_k_nearest_neighbours(cities, matrix, K_NEAREST)
    print_k_nearest(cities, neighbours)

    print_header("RUNNING HEURISTIC FROM EVERY STARTING LOCATION")
    best, all_results = find_best_route(cities, matrix, neighbours)

    for start_index, tour, cost, steps in all_results:
        route_names = " -> ".join([cities[idx] for idx in tour])
        marker = "  <-- BEST" if start_index == best[0] else ""
        print(f"\nStart: {cities[start_index]:<25} Total Cost: {cost:>8.1f} m{marker}")
        print(f"  Route: {route_names}")

    print_header("BEST ROUTE FOUND")
    best_start, best_tour, best_cost, best_steps = best
    print(f"Starting Location : {cities[best_start]}")
    print("\n--- Step-by-Step Traversal ---")
    print_step_details(cities, best_steps)

    route_names = " -> ".join([cities[idx] for idx in best_tour])
    print("\n--- Final Route & Cost Summary ---")
    print(f"Full Tour   : {route_names}")
    print(f"Total Cost  : {best_cost:.1f} metres (~{best_cost/1000:.2f} km)")
    print("=" * 60)


if __name__ == "__main__":
    main()