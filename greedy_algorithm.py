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

Note: Standard insertion sort (via array shifting) is implemented
manually to satisfy the requirement of not using built-in sort functions.

Validation (added):
Before scheduling, every request is checked against a set of
constraints. Any request that breaks a constraint is REJECTED at the
validation stage (with a reason) and never reaches the greedy
algorithm at all, so bad data cannot silently corrupt the schedule.
"""

import re

# ---------------------------------------------------------------------
# Hardcoded problem data: requested lecture hall bookings for one day.
# A few deliberately BROKEN entries (C11-C14) are included so the
# validation step below has something to catch and demonstrate.
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
    # --- deliberately invalid rows, to prove validation works ---
    ["C11", "CSC2999", "Broken: finish before start", "2026-08-03", "15:00", "14:00"],
    ["C12", "CSC2998", "Broken: bad time format", "2026-08-03", "9am", "10:00"],
    ["C13", "", "Broken: missing course code", "2026-08-03", "10:00", "11:00"],
    ["C1", "CSC2997", "Broken: duplicate Class ID (C1 used above)", "2026-08-03", "07:00", "07:30"],
]

TIME_PATTERN = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")  # strict 24-hour HH:MM


# ---------------------------------------------------------------------
# CONSTRAINTS / VALIDATION
# ---------------------------------------------------------------------
def validate_requests(requests, log=None):
    """
    Applies data-integrity constraints to the raw request list and
    splits it into (valid, invalid) lists.

    Constraints enforced:
      1. Class ID, Course Code, Description, Date must all be non-empty.
      2. Class ID must be unique across the whole roster.
      3. Start and Finish must match strict 24-hour "HH:MM" format.
      4. Start time must be strictly earlier than Finish time
         (zero-length or negative-length bookings are rejected).

    requests: raw list of [id, course, description, date, start, finish]
    log: optional list to record [Class ID, Decision, Reason]
    returns: (valid_requests, invalid_requests)
    """
    valid = []
    invalid = []
    seen_ids = set()

    for r in requests:
        class_id, course, description, date, start, finish = r
        reasons = []

        # Constraint 1: required fields not empty
        if not class_id.strip():
            reasons.append("Class ID is empty")
        if not course.strip():
            reasons.append("Course code is empty")
        if not description.strip():
            reasons.append("Description is empty")
        if not date.strip():
            reasons.append("Date is empty")

        # Constraint 2: unique Class ID
        if class_id in seen_ids:
            reasons.append(f"Duplicate Class ID '{class_id}'")

        # Constraint 3: valid HH:MM 24-hour format
        start_ok = bool(TIME_PATTERN.match(start))
        finish_ok = bool(TIME_PATTERN.match(finish))
        if not start_ok:
            reasons.append(f"Start time '{start}' is not valid 24-hour HH:MM")
        if not finish_ok:
            reasons.append(f"Finish time '{finish}' is not valid 24-hour HH:MM")

        # Constraint 4: start must be strictly before finish
        # (only checked when both times are well-formed, else comparison
        # itself would be meaningless)
        if start_ok and finish_ok and start >= finish:
            reasons.append(f"Start time '{start}' is not before finish time '{finish}'")

        if reasons:
            invalid.append(r)
            if log is not None:
                log.append([class_id or "(blank)", "INVALID", "; ".join(reasons)])
        else:
            valid.append(r)
            seen_ids.add(class_id)
            if log is not None:
                log.append([class_id, "VALID", "Passed all constraints"])

    return valid, invalid


def manual_sort_by_finish_time(requests):
    """
    Sorts a list of class requests [id, course, description, date, start, finish]
    in ascending order of finish time using standard Insertion Sort.
    Finish times are "HH:MM" strings, which compare lexicographically.
    """
    lst = [r[:] for r in requests]

    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and lst[j][5] > key[5]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key

    return lst


def select_roster(sorted_requests, log=None):
    """
    Applies the greedy algorithm to select the maximum number of
    non-overlapping class bookings from an ALREADY SORTED, ALREADY
    VALIDATED list of requests.
    """
    if not sorted_requests:
        return []

    selected = [sorted_requests[0]]
    last_finish_time = sorted_requests[0][5]

    if log is not None:
        log.append([sorted_requests[0][0], "ACCEPTED", "Hall is free"])

    for i in range(1, len(sorted_requests)):
        current = sorted_requests[i]
        start_time = current[4]

        if start_time >= last_finish_time:
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


def print_decision_log(title, log, col2="Decision"):
    print(f"\n{title}")
    header = f"{'Class':<8}| {col2:<10}| {'Reason':<55}"
    print(header)
    print("-" * len(header))
    for class_id, decision, reason in log:
        print(f"{class_id:<8}| {decision:<10}| {reason:<55}")


def main():
    print("=" * 60)
    print("    LECTURE HALL ROSTER SCHEDULING (GREEDY - ACTIVITY SELECTION)")
    print("=" * 60)

    print("\nProblem:")
    print("  One lecture hall is available. Several classes have each")
    print("  requested a time slot on the same day, but some of those")
    print("  slots overlap - the hall can only host one class at a time.")
    print("  Goal: schedule the MAXIMUM number of non-overlapping classes.")

    print_table("All Requested Bookings (raw, includes bad data):", ROSTER_REQUESTS)

    print("\nStep 0 - Validate constraints:")
    print("  Every request must have all fields filled in, a unique Class ID,")
    print("  properly formatted 24-hour HH:MM times, and Start < Finish.")
    print("  Anything that fails is rejected here and never reaches scheduling.")
    validation_log = []
    valid_requests, invalid_requests = validate_requests(ROSTER_REQUESTS, log=validation_log)
    print_decision_log("Validation Results:", validation_log, col2="Status")

    if invalid_requests:
        print(f"\n{len(invalid_requests)} request(s) rejected at validation and excluded from scheduling.")

    print("\nStep 1 - Sort by finish time:")
    print("  Every VALID request is sorted so the class that finishes EARLIEST")
    print("  comes first. Considering early finishers first leaves the")
    print("  most remaining time in the day for other classes.")
    sorted_requests = manual_sort_by_finish_time(valid_requests)
    print_table("Valid Requests Sorted by Finish Time:", sorted_requests)

    print("\nStep 2 - Greedily accept or reject each class in that order:")
    print("  A class is ACCEPTED only if its start time is not earlier")
    print("  than the finish time of the last class already booked into")
    print("  the hall (i.e. it does not clash with the current booking).")
    decision_log = []
    selected = select_roster(sorted_requests, log=decision_log)
    print_decision_log("Accept / Reject Decisions:", decision_log)

    print_table("Final Lecture Hall Roster (Optimal Schedule):", selected)

    print(f"\nMaximum number of classes that can use the hall: {len(selected)}")
    print("Roster order:", " -> ".join(r[0] for r in selected))
    print("\nWhy this is optimal: this is the classic Activity Selection")
    print("problem. Always picking the next class with the earliest")
    print("finish time (and skipping anything that clashes) is proven to")
    print("never do worse than any other selection order, so the count")
    print("of classes scheduled above is the maximum possible.")


if __name__ == "__main__":
    main()
