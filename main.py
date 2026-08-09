"""
CSC2103 Group Project - menu launcher
=====================================
Optional single entry point that lets you run all three programs from one
menu. Each problem also runs on its own, e.g.:

    python3 problem1_activity_selection.py
    python3 problem2_mazepathfinder.py
    python3 problem3_tsp_heuristic.py
    python3 main.py                     # this menu
"""

import problem1_activityselection as p1
import problem2_mazepathfinder as p2
import problem3_tsp_heuristic as p3



def box(rows):
    """Create a simple box around menu items."""
    max_len = max(len(str(row)) for row in rows)
    border = "+" + "-" * (max_len + 4) + "+"
    result = [border]
    for row in rows:
        result.append("|  " + str(row).ljust(max_len) + "  |")
    result.append(border)
    return "\n".join(result)


def read_line(prompt):
    """Get user input with a prompt."""
    return input(prompt)


# Main menu
MENU = {
    "1": ("Activity Selection      (Greedy)", p1.run),
    "2": ("Maze Path Finder        (Backtracking)", p2.run),
    "3": ("Travelling Salesman     (Heuristic)", p3.run),
}


def print_menu():
    rows = ["Main Menu", ""]
    for key, (label, _) in MENU.items():
        rows.append(f"[{key}]  {label}")
    rows.append("[0]  Exit")
    print(box(rows))


def main():
    print("\nCSC2103: Data Structures and Algorithms- Group Project")
    print("=" * 50)
    while True:
        print_menu()
        choice = read_line("Pick a problem: ").strip()

        if choice == "0":
            print("\n  Bye bye!")
            break

        if choice in MENU:
            try:
                MENU[choice][1]()
            except Exception as e:
                print(f"\n  -> Something went wrong while running this program: {e}")
            input("\nPress Enter to return to the menu...")
        else:
            print("  -> Invalid option, please choose 1, 2, 3 or 0!")


main()