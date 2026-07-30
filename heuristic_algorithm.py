"""
Notes
algo to find travel from any vertex to nearest neighbor until all vertexes are passed
https://www.youtube.com/watch?v=ojjnd5gEMuk
"""

def print_header(title):
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50)


def print_matrix(cities, matrix):
    """Displays the distance matrix as a formatted table."""
    print("\n--- Distance Matrix ---")
    header = f"{'':<12}" + "".join([f"{city[:10]:<12}" for city in cities])
    print(header)
    print("-" * len(header))
    
    for i, row in enumerate(matrix):
        row_str = f"{cities[i][:10]:<12}" + "".join([f"{dist:<12}" for dist in row])
        print(row_str)


def nearest_neighbour_tsp(distance_matrix, start_index=0):
    """
    Solves TSP using the Nearest Neighbour Heuristic.
    Time Complexity: O(V^2)
    Space Complexity: O(V)
    """
    num_cities = len(distance_matrix)
    visited = [False] * num_cities
    tour = [start_index]
    visited[start_index] = True
    
    current_city = start_index
    total_cost = 0
    step_details = []
    
    # Visit all remaining (num_cities - 1) cities
    for _ in range(num_cities - 1):
        nearest_city = None
        min_distance = float('inf')
        
        # Search for the closest unvisited neighbor
        for next_city in range(num_cities):
            if not visited[next_city] and distance_matrix[current_city][next_city] < min_distance:
                min_distance = distance_matrix[current_city][next_city]
                nearest_city = next_city
        
        # Record step for summary
        step_details.append((current_city, nearest_city, min_distance))
        
        # Move to nearest neighbor
        visited[nearest_city] = True
        tour.append(nearest_city)
        total_cost += min_distance
        current_city = nearest_city
        
    # Return to the starting city to complete the cycle
    return_distance = distance_matrix[current_city][start_index]
    total_cost += return_distance
    tour.append(start_index)
    step_details.append((current_city, start_index, return_distance))
    
    return tour, total_cost, step_details


def get_default_dataset():
    """Returns a pre-configured sample dataset for testing."""
    cities = ["Kuala Lumpur", "Penang", "Johor Bahru", "Ipoh", "Melaka"]
    matrix = [
        [0, 350, 330, 200, 150],
        [350, 0, 680, 160, 500],
        [330, 680, 0, 530, 210],
        [200, 160, 530, 0, 350],
        [150, 500, 210, 350, 0]
    ]
    return cities, matrix


def get_user_dataset():
    """Handles manual user input for cities and distances."""
    print_header("MANUAL DATA ENTRY")
    
    while True:
        try:
            num_cities = int(input("Enter number of cities (minimum 3): "))
            if num_cities >= 3:
                break
            print("Please enter at least 3 cities.")
        except ValueError:
            print("Invalid input! Please enter an integer number.")

    cities = []
    print("\n--- Enter City Names ---")
    for i in range(num_cities):
        name = input(f"Enter name for City {i + 1}: ").strip()
        if not name:
            name = f"City_{i + 1}"
        cities.append(name)

    print("\n--- Enter Distance Matrix ---")
    print("Note: Enter distances between cities. Distance from a city to itself is 0.")
    
    matrix = [[0] * num_cities for _ in range(num_cities)]
    
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            while True:
                try:
                    dist = float(input(f"Distance from {cities[i]} to {cities[j]}: "))
                    if dist >= 0:
                        matrix[i][j] = dist
                        matrix[j][i] = dist  # Symmetric matrix assumption
                        break
                    print("Distance cannot be negative.")
                except ValueError:
                    print("Invalid input! Please enter a numerical distance.")

    return cities, matrix


def main():
    print_header("CSC2103: TSP NEAREST NEIGHBOUR HEURISTIC")
    print("1. Use Sample Dataset (5 Cities)")
    print("2. Enter Custom Dataset")
    
    choice = input("\nSelect an option (1 or 2): ").strip()
    
    if choice == "2":
        cities, matrix = get_user_dataset()
    else:
        print("\n[INFO] Loading Default Dataset...")
        cities, matrix = get_default_dataset()

    # Display Input Matrix
    print_matrix(cities, matrix)

    # Choose Start City
    print("\n--- Select Starting City ---")
    for idx, city in enumerate(cities):
        print(f"{idx}: {city}")
        
    while True:
        try:
            start_idx = int(input(f"Enter start city index (0 to {len(cities)-1}): "))
            if 0 <= start_idx < len(cities):
                break
            print("Index out of bounds!")
        except ValueError:
            print("Please enter a valid integer index.")

    # Execute Heuristic Algorithm
    tour, total_cost, step_details = nearest_neighbour_tsp(matrix, start_idx)

    # --- OUTPUT DISPLAY ---
    print_header("SOLUTION & EXECUTION SUMMARY")
    
    print("\n--- Step-by-Step Traversal ---")
    print(f"{'From':<15} {'To':<15} {'Distance':<10}")
    print("-" * 40)
    for from_node, to_node, dist in step_details:
        print(f"{cities[from_node]:<15} {cities[to_node]:<15} {dist:<10}")

    print("\n--- Final Route & Cost Summary ---")
    route_names = " -> ".join([cities[idx] for idx in tour])
    print(f"Full Tour   : {route_names}")
    print(f"Total Cost  : {total_cost:.2f} units")
    print("=" * 50)


if __name__ == "__main__":
    main()
