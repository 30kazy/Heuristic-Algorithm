"""
Lecture Hall Roster Scheduling - Greedy Algorithm (Activity Selection)
------------------------------------------------------------------------
Problem: A university has ONE lecture hall. Several classes have
requested to use it on the same day, but some of their requested time
slots overlap. Given each class's requested start time and finish
time, select the MAXIMUM number of classes that can be scheduled into
the hall without any two classes overlapping.

Greedy Choice: At each step, always pick the class that finishes
EARLIEST among the classes still compatible with what has already
been scheduled. Finishing early leaves the most room in the roster
for other classes, which is why this greedy choice leads to an
optimal (maximum-count) solution.

Note: No built-in sort() / sorted() is used for the core logic - the
sort by finish time is implemented manually (insertion sort) since the
assignment requires the algorithmic logic to be written by hand.

No user input is required - the class requests are hardcoded below,
and the program simply shows the problem and solves it.
"""


# ---------------------------------------------------------------------
# Hardcoded problem data: requested lecture hall bookings for one day.
# Each entry: [Class ID, Course Code, Course Description, Date,
#              Start Time, Finish Time]
# Start/Finish are given in 24-hour "HH:MM" format.
# ---------------------------------------------------------------------
ROSTER_REQUESTS = [
    ["C1", "CSC2014", "Data Structures & Image Processing", "2026-08-03", "08:00", "09:30"],
    ["C2", "MPU3332", "Integrity and Anti-Corruption", "2026-08-03", "09:00", "10:30"],
    ["C3", "CSC2103", "Data Structures and Algorithms", "2026-08-03", "09:45", "11:00"],
    ["C4", "ENG1010", "Communication Skills", "2026-08-03", "11:00", "12:30"],
    ["C5", "CSC2014", "Data Structures & Image Processing", "2026-08-03", "12:00", "13:00"],
    ["C6", "MPU3332", "Integrity and Anti-Corruption", "2026-08-03", "13:00", "14:30"],
    ["C7", "CSC2103", "Data Structures and Algorithms", "2026-08-03", "13:30", "15:00"],
    ["C8", "ENG1010", "Communication Skills", "2026-08-03", "14:45", "16:00"],
    ["C9", "CSC2014", "Data Structures & Image Processing", "2026-08-03", "16:00", "17:00"],
    ["C10", "MPU3332", "Integrity and Anti-Corruption", "2026-08-03", "16:30", "18:00"],
]


def manual_sort_by_finish_time(requests):
    """
    Sorts a list of class requests
    [id, course, description, date, start, finish] in ascending order
    of finish time using insertion sort (implemented manually, no
    built-in sort library used). Finish times are "HH:MM" strings,
    which compare correctly with normal string comparison since they
    are zero-padded 24-hour format.
    """
    lst = requests[:]  # copy so we don't mutate the original

    for i in range(1, len(lst)):
        key = lst[i]
        lst.pop(i)

        inserted = False
        for j in range(i):
            if key[5] < lst[j][5]:  # compare by finish time (index 5)
                lst.insert(j, key)
                inserted = True
                break

        if not inserted:
            lst.insert(i, key)

    return lst


def select_roster(requests, log=None):
    """
    Applies the greedy algorithm to select the maximum number of
    non-overlapping class bookings for the lecture hall.

    requests: list of [Class ID, Course, Description, Date, Start, Finish]
    log: optional list - if provided, one row is appended per class
         request in the form [Class ID, Decision, Reason], so the
         decisions can be printed neatly as a table afterwards
    returns: list of selected classes, in the order they were chosen
    """
    if not requests:
        return []

    # Step 1: Sort requests by finish time (greedy ordering)
    sorted_requests = manual_sort_by_finish_time(requests)

    # Step 2: Always select the first class (earliest finish time),
    #          since there is nothing booked yet to clash with it.
    selected = [sorted_requests[0]]
    last_finish_time = sorted_requests[0][5]

    if log is not None:
        log.append([sorted_requests[0][0], "ACCEPTED", "Hall is free"])

    # Step 3: Walk through the rest, greedily picking any class whose
    #          start time is >= the finish time of the last class we
    #          selected (i.e. it doesn't clash with the hall booking)
    for i in range(1, len(sorted_requests)):
        current = sorted_requests[i]
        if current[4] >= last_finish_time:
            selected.append(current)
            if log is not None:
                log.append([current[0], "ACCEPTED", f"Starts at/after {last_finish_time}"])
            last_finish_time = current[5]
        else:
            if log is not None:
                log.append([current[0], "REJECTED", f"Clashes until {last_finish_time}"])

    return selected


def print_table(title, requests):
    print(f"\n{title}")
    header = (f"{'Class':<8}| {'Course':<10}| {'Description':<38}"
              f"| {'Date':<12}| {'Start':<8}| {'Finish':<8}")
    print(header)
    print("-" * len(header))
    for r in requests:
        print(f"{r[0]:<8}| {r[1]:<10}| {r[2]:<38}| {r[3]:<12}| {r[4]:<8}| {r[5]:<8}")


def print_decision_log(title, log):
    print(f"\n{title}")
    header = f"{'Class':<8}| {'Decision':<12}| {'Reason':<28}"
    print(header)
    print("-" * len(header))
    for class_id, decision, reason in log:
        print(f"{class_id:<8}| {decision:<12}| {reason:<28}")


def main():
    print("=" * 60)
    print("   LECTURE HALL ROSTER SCHEDULING (GREEDY - ACTIVITY SELECTION)")
    print("=" * 60)

    print("\nProblem:")
    print("  One lecture hall is available. Several classes have each")
    print("  requested a time slot on the same day, but some of those")
    print("  slots overlap - the hall can only host one class at a time.")
    print("  Goal: schedule the MAXIMUM number of non-overlapping classes.")

    print_table("All Requested Bookings:", ROSTER_REQUESTS)

    print("\nStep 1 - Sort by finish time:")
    print("  Every request is sorted so the class that finishes EARLIEST")
    print("  comes first. Considering early finishers first leaves the")
    print("  most remaining time in the day for other classes.")
    sorted_requests = manual_sort_by_finish_time(ROSTER_REQUESTS)
    print_table("Requests Sorted by Finish Time:", sorted_requests)

    print("\nStep 2 - Greedily accept or reject each class in that order:")
    print("  A class is ACCEPTED only if its start time is not earlier")
    print("  than the finish time of the last class already booked into")
    print("  the hall (i.e. it does not clash with the current booking).")
    decision_log = []
    selected = select_roster(ROSTER_REQUESTS, log=decision_log)
    print_decision_log("Accept / Reject Decisions:", decision_log)

    print_table("\nFinal Lecture Hall Roster (Optimal Schedule):", selected)

    print(f"\nMaximum number of classes that can use the hall: {len(selected)}")
    print("Roster order:", " -> ".join(r[0] for r in selected))
    print("\nWhy this is optimal: this is the classic Activity Selection")
    print("problem. Always picking the next class with the earliest")
    print("finish time (and skipping anything that clashes) is proven to")
    print("never do worse than any other selection order, so the count")
    print("of classes scheduled above is the maximum possible.")


if __name__ == "__main__":
    main()
