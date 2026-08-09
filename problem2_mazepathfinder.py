import random 
"""used during maze generation for walls"""



def get_valid_input(prompt, min_val, max_val):
    """Keeps asking the user for a number until they give a valid one in range."""
    while True:
        try:
            user_input = int(input(prompt))
            if min_val <= user_input <= max_val:
                return user_input
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def is_safe(maze, x, y, visited):
    """Checks whether we're allowed to step onto this cell.
    It has to be inside the grid, not a wall, and not somewhere we've already been."""
    rows = len(maze)
    cols = len(maze[0])
    return 0 <= x < rows and 0 <= y < cols and maze[x][y] != 1 and not visited[x][y]

def maze_has_solution(maze, start_x, start_y, end_x, end_y):
    """Does a quick flood fill just to check if the end can be reached at all.
    This is separate from find_path, it only answers yes or no, it doesn't draw anything."""
    rows = len(maze)
    cols = len(maze[0])
    checked = [[False for _ in range(cols)] for _ in range(rows)]
    stack = [(start_x, start_y)]
    checked[start_x][start_y] = True

    while stack:
        x, y = stack.pop()
        if x == end_x and y == end_y:
            return True
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1 and not checked[nx][ny]:
                checked[nx][ny] = True
                stack.append((nx, ny))

    return False

def find_path(maze, x, y, end_x, end_y, visited, path_board):
    """The actual backtracking solver. Walks the maze one step at a time and
    backs itself out of dead ends until it either finds the exit or runs out of options."""
    if x == end_x and y == end_y:
        path_board[x][y] = 'E'
        return True

    if is_safe(maze, x, y, visited):
        visited[x][y] = True
        if path_board[x][y] != 'S': #start point
            path_board[x][y] = '*' #path taken

        if find_path(maze, x + 1, y, end_x, end_y, visited, path_board): return True #down
        if find_path(maze, x, y + 1, end_x, end_y, visited, path_board): return True #right 
        if find_path(maze, x - 1, y, end_x, end_y, visited, path_board): return True #up
        if find_path(maze, x, y - 1, end_x, end_y, visited, path_board): return True #left 

        if path_board[x][y] != 'S':
            path_board[x][y] = '.' # Backtrack happens here as the mark path ('*') changes back to open space ('.') since no valid path was found from here
        return False

    return False

def setup_maze():
    """Builds the maze from scratch based on whatever the user tells us.
    Also makes sure the maze it hands back is actually solvable before returning it."""
    print("=" * 50)
    print("MAZE PATH FINDER - BACKTRACKING ALGORITHM".center(50))
    print("=" * 50)
    print("\nLet's set up your maze!\n")
    
    rows = get_valid_input("Enter number of rows (3-20): ", 3, 20)
    cols = get_valid_input("Enter number of columns (3-20): ", 3, 20)

    print("\nHow many walls should the maze have?")
    density = get_valid_input("Enter wall density percentage (10-40%): ", 10, 40)

    print("\nNow let's set your start point.")
    start_x = get_valid_input(f"Enter Start Row (0 to {rows-1}): ", 0, rows - 1)
    start_y = get_valid_input(f"Enter Start Column (0 to {cols-1}): ", 0, cols - 1)

    print("\nAnd now your end point.")
    while True:
        end_x = get_valid_input(f"Enter End Row (0 to {rows-1}): ", 0, rows - 1)
        end_y = get_valid_input(f"Enter End Column (0 to {cols-1}): ", 0, cols - 1)
        if end_x == start_x and end_y == start_y:
            print(f"End point can't be the same as the start point at ({start_x}, {start_y}). Try again.")
        else:
            break
        
    total_cells = rows * cols 
    num_walls = int((density / 100) * total_cells)

    # We regenerate the walls if this attempt boxes in the start or end completely.
    # Random placement alone can't guarantee a path exists, so we check every time.
    max_attempts = 200 
    for attempt in range(1, max_attempts + 1):
        maze = [[0 for _ in range(cols)] for _ in range(rows)]

        walls_placed = 0
        while walls_placed < num_walls: 
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            if maze[r][c] == 0:
                maze[r][c] = 1
                walls_placed += 1

        maze[start_x][start_y] = 0
        maze[end_x][end_y] = 0

        if maze_has_solution(maze, start_x, start_y, end_x, end_y):
            if attempt > 1:
                print(f"\nNeeded {attempt} tries to land on a maze that's actually solvable.")
            break
    else:
        print(f"\nCouldn't generate a solvable maze after {max_attempts} tries, try a lower wall density.")

    return maze, rows, cols, start_x, start_y, end_x, end_y

def print_maze(path_board, title):
    """Prints the maze inside a border"""
    width = len(path_board[0]) * 2 + 1
    print("\n" + "-" * (width + 2))
    print(f"|{title.center(width)}|")
    print("-" * (width + 2))
    for row in path_board:
        print("| " + " ".join(str(cell) for cell in row) + " |")
    print("-" * (width + 2))


def run():
    maze, rows, cols, start_x, start_y, end_x, end_y = setup_maze()

    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path_board = [['.' if maze[r][c] == 0 else '#' for c in range(cols)] for r in range(rows)]
    path_board[start_x][start_y] = 'S'
    path_board[end_x][end_y] = 'E'

    print("\nKEYWORDS:  S = Start   E = End   # = Wall   . = Open Path   * = Solved Path")

    print_maze(path_board, "GENERATED MAZE")

    print("\nCalculating path...")

    if find_path(maze, start_x, start_y, end_x, end_y, visited, path_board):
        print("\nA path was found! '*' marks the path from start to end.")
        print_maze(path_board, "SOLVED MAZE")
    else:
        print("\nNo valid path exists in this generated maze.")

    print("\n" + "=" * 50)
    print("Program finished! BYE".center(50))
    print("=" * 50)


if __name__ == "__main__":
    run()