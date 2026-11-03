# =============================================================================
# EduSense: A Console-Based Student Grade Calculator
# ITE 260 – Computer Programming 1 | Section: FB2-BSIT1-03
# Group 6 — Buagan, Ebal, Maglot, Tolomia, Ugmad
# =============================================================================
# Purpose:
# Record assessment scores, calculate component averages and weighted grades,
# and display individual and class-level academic results.
#
# Grade-entry flow:
# Teacher Login -> Student -> Period -> Component -> Scores -> Save
#
# Grading periods:
# P1 = Modules 1-4 | P2 = Modules 5-9 | P3 = Modules 10-14
#
# Data is stored in memory and resets when the program is closed.
# =============================================================================

import math


# ==========================================
# 1. CONSTANTS
# ==========================================

PASSING_GRADE = 80

COMPONENT_NAMES = [
    "Start of Class Attendance",
    "Let's Practice",
    "Reflection",
    "Wrap-up Quiz",
    "Check-in Project",
]

# Keep the same order as COMPONENT_NAMES for the weighted-grade calculation.
COMPONENT_WEIGHTS = [5, 35, 15, 15, 30]

# Fixed maximum score for each activity entry, as defined in the project scope.
COMPONENT_MAX_SCORES = {
    "Start of Class Attendance": 3,
    "Let's Practice": 3,
    "Reflection": 3,
    "Wrap-up Quiz": 7,
    "Check-in Project": 100,
}

PERIODS = ["P1", "P2", "P3"]

PERIOD_DESCRIPTIONS = {
    "P1": "Modules 1-4",
    "P2": "Modules 5-9",
    "P3": "Modules 10-14",
}

# Required number of activities for each component in each grading period.
# These counts are also used as the denominator even when fewer scores are entered.
PERIOD_ACTIVITY_COUNTS = {
    "P1": {
        "Start of Class Attendance": 8,
        "Let's Practice": 4,
        "Reflection": 4,
        "Wrap-up Quiz": 4,
        "Check-in Project": 1,
    },
    "P2": {
        "Start of Class Attendance": 10,
        "Let's Practice": 5,
        "Reflection": 5,
        "Wrap-up Quiz": 5,
        "Check-in Project": 1,
    },
    "P3": {
        "Start of Class Attendance": 10,
        "Let's Practice": 5,
        "Reflection": 5,
        "Wrap-up Quiz": 5,
        "Check-in Project": 1,
    },
}

SEPARATOR = "=" * 68
THIN_SEPARATOR = "-" * 68


def print_header(title):
    """Print a centered section heading between full separator lines."""
    print("\n" + SEPARATOR)
    print(title.center(len(SEPARATOR)))
    print(SEPARATOR)


# ==========================================
# 2. USER AND STUDENT RECORDS
# ==========================================

# User record: [ID, Password, Role, Full Name]
# Credentials are predefined for this project prototype.
users = [
    ["T001", "teacher123", "teacher", "Teacher"],
    ["2026-001", "lea123", "student", "Lea Jane D. Tolomia"],
    ["2026-002", "kevin123", "student", "Kevin Dave Ebal"],
    ["2026-003", "charinel123", "student", "Charinel V. Buagan"],
    ["2026-004", "bryan123", "student", "Bryan Jacob Ugmad"],
    ["2026-005", "chazzel123", "student", "Chazzel Stephanie MAGLOT"],
]


def create_empty_grade_data():
    """Create empty component records for P1, P2, and P3."""
    grade_data = {}

    for period in PERIODS:
        grade_data[period] = {}
        for component in COMPONENT_NAMES:
            # None means the teacher has not entered this component yet.
            # An empty list means the teacher intentionally left it blank (0 points).
            grade_data[period][component] = None

    return grade_data


# Student record: [Student ID, Full Name, Grade Data]
students = [
    [user[0], user[3], create_empty_grade_data()]
    for user in users
    if user[2] == "student"
]


# ==========================================
# 3. INPUT VALIDATION
# ==========================================


def get_valid_choice(prompt, minimum, maximum):
    """Return a valid whole-number menu choice."""
    while True:
        try:
            choice = int(input(prompt).strip())
            if minimum <= choice <= maximum:
                return choice
            print(f"Invalid choice. Select a number from {minimum} to {maximum}.")
        except ValueError:
            print("Invalid choice. Please enter a whole number.")


def get_scores_on_one_line(max_score, component_name, required_count):
    """Accept blank input or up to the required number of valid whole-number scores."""
    while True:
        scores_input = input(f"Enter scores for {component_name}: ").strip()

        # A blank line is accepted and records zero earned points for this component.
        if not scores_input:
            return []

        tokens = scores_input.split()
        if len(tokens) > required_count:
            print(
                f"Too many scores. Enter no more than {required_count} "
                f"scores for {component_name}."
            )
            continue

        scores = []
        valid_input = True

        for token in tokens:
            try:
                earned = float(token)
            except ValueError:
                print(
                    f"Invalid score '{token}'. Use whole numbers from 0 to {max_score}."
                )
                valid_input = False
                break

            if (
                not math.isfinite(earned)
                or not earned.is_integer()
                or earned < 0
                or earned > max_score
            ):
                print(
                    f"Invalid score '{token}'. Use a whole number from 0 to {max_score}."
                )
                valid_input = False
                break

            scores.append([int(earned), max_score])

        # Reject the complete entry if even one score is invalid.
        if valid_input:
            return scores


def find_user(user_id, password, role):
    """Find a user by ID, password, and role."""
    for user in users:
        if user[0] == user_id and user[1] == password and user[2] == role:
            return user
    return None


def find_student(student_id):
    """Find a student record by student ID."""
    for student in students:
        if student[0] == student_id:
            return student
    return None


# ==========================================
# 4. GRADE CALCULATIONS
# ==========================================


def calc_component_average(score_array, period, component_name):
    """Calculate a component percentage using the full required activity count."""
    if score_array is None:
        return None

    total_score = sum(pair[0] for pair in score_array)
    required_count = PERIOD_ACTIVITY_COUNTS[period][component_name]
    max_per_activity = COMPONENT_MAX_SCORES[component_name]
    total_possible = required_count * max_per_activity

    if total_possible <= 0:
        return None

    return (total_score / total_possible) * 100


def calc_period_grade(period_data, period):
    """Calculate the weighted period grade when all components have been entered."""
    total_grade = 0

    for index, component in enumerate(COMPONENT_NAMES):
        weight = COMPONENT_WEIGHTS[index]
        average = calc_component_average(period_data[component], period, component)

        if average is None:
            return None

        total_grade += (average / 100) * weight

    return round(total_grade, 2)


def calc_final_grade(student_data):
    """Average P1, P2, and P3; return None if any period is incomplete."""
    period_grades = []

    for period in PERIODS:
        grade = calc_period_grade(student_data[period], period)
        if grade is None:
            return None
        period_grades.append(grade)

    return round(sum(period_grades) / len(period_grades), 2)


def get_academic_status(final_grade):
    """Classify the final result as Passed, Failed, or Incomplete."""
    if final_grade is None:
        return "Incomplete"
    if final_grade >= PASSING_GRADE:
        return "Passed"
    return "Failed"


def calculate_all_period_grades(student):
    """Return a dictionary containing the student's P1, P2, and P3 grades."""
    return {
        period: calc_period_grade(student[2][period], period)
        for period in PERIODS
    }


def format_grade(grade):
    """Display a grade with two decimal places or Incomplete."""
    return "Incomplete" if grade is None else f"{grade:.2f}"


def format_percentage(percentage):
    """Display a percentage with two decimal places or Incomplete."""
    return "Incomplete" if percentage is None else f"{percentage:.2f}%"


def get_missing_components(period_data):
    """Return components the teacher has not entered yet (None, not a blank entry)."""
    return [component for component in COMPONENT_NAMES if period_data[component] is None]


# ==========================================
# 5. GRADE ENTRY
# ==========================================


def display_selected_student_status(student):
    """Display the selected student's current period and final-grade status."""
    period_grades = calculate_all_period_grades(student)
    final_grade = calc_final_grade(student[2])

    print_header("STUDENT GRADE STATUS")
    print(f"ID: {student[0]}   Name: {student[1]}")
    print(f"{'Period':<8}{'Coverage':<20}{'Grade':>14}{'Status':>16}")
    print(THIN_SEPARATOR)

    for period in PERIODS:
        grade = period_grades[period]
        print(
            f"{period:<8}{PERIOD_DESCRIPTIONS[period]:<20}"
            f"{format_grade(grade):>14}{get_academic_status(grade):>16}"
        )

    print(THIN_SEPARATOR)
    print(f"{'Final Grade':<28}{format_grade(final_grade):>18}")
    print(f"{'Academic Status':<28}{get_academic_status(final_grade):>18}")


def enter_component_scores(component_name, period):
    """Enter and immediately save scores for one component."""
    max_score = COMPONENT_MAX_SCORES[component_name]
    required_count = PERIOD_ACTIVITY_COUNTS[period][component_name]
    scores = get_scores_on_one_line(max_score, component_name, required_count)

    total_earned = sum(score[0] for score in scores)
    total_possible = required_count * max_score
    average = calc_component_average(scores, period, component_name)

    print(f"Saved: {total_earned}/{total_possible} | Average: {average:.2f}%")
    return scores

def enter_period_grades():
    """Select a student and period, then enter all five components in order."""
    while True:
        print_header("ENTER GRADES")
        student_id = input("Student ID: ").strip()

        # Invalid ID input returns directly to the Teacher Menu without extra prompts.
        if (
            student_id.count("-") != 1
            or not student_id.replace("-", "").isdigit()
            or len(student_id.split("-")[0]) != 4
            or len(student_id.split("-")[1]) != 3
        ):
            return

        student = find_student(student_id)

        if student is None:
            print("Student not found. Check the Student List and try again.")
            retry_choice = get_valid_choice(
                "[1] Try Another Student\n[2] Return to Teacher Menu\nSelect an option: ",
                1,
                2,
            )
            if retry_choice == 2:
                return
            continue

        print(f"\nSelected Student: {student[1]} ({student[0]})")
        display_selected_student_status(student)

        while True:
            print_header("SELECT GRADING PERIOD")
            for index, period in enumerate(PERIODS, start=1):
                print(f"[{index}] {period} - {PERIOD_DESCRIPTIONS[period]}")
            print("[4] Back to Student Selection")
            print("[5] Exit Grade Entry and Return to Teacher Menu")

            period_choice = get_valid_choice("Select an option: ", 1, 5)
            if period_choice == 4:
                break
            if period_choice == 5:
                return

            selected_period = PERIODS[period_choice - 1]
            period_data = {}
            print_header(f"ENTER {selected_period} GRADES — {PERIOD_DESCRIPTIONS[selected_period]}")

            # No component menu or save confirmation: enter all five components in order.
            for component in COMPONENT_NAMES:
                scores = enter_component_scores(component, selected_period)
                period_data[component] = scores

            # Save the complete period after all five components have valid entries.
            student[2][selected_period] = period_data
            period_grade = calc_period_grade(period_data, selected_period)
            print("\nAll component grades saved successfully.")
            print(f"{selected_period} Grade: {format_percentage(period_grade)}")
            display_selected_student_status(student)

def display_period_section(student, period):
    """Display component averages, weights, activity counts, and period grade."""
    period_data = student[2][period]
    print_header(f"{period} — {PERIOD_DESCRIPTIONS[period]}")
    print(
        f"{'Component':<30}{'Weight':>9}{'Activities':>13}{'Average':>16}"
    )
    print(THIN_SEPARATOR)

    for index, component in enumerate(COMPONENT_NAMES):
        scores = period_data[component]
        average = calc_component_average(scores, period, component)
        weight = COMPONENT_WEIGHTS[index]
        activities_entered = "—" if scores is None else str(len(scores))
        required_count = PERIOD_ACTIVITY_COUNTS[period][component]
        activity_label = f"{activities_entered}/{required_count}"
        print(
            f"{component:<30}{weight:>8}%{activity_label:>13}"
            f"{format_percentage(average):>16}"
        )

    period_grade = calc_period_grade(period_data, period)
    print(f"Period Grade: {format_percentage(period_grade)}")
    print(f"Academic Status: {get_academic_status(period_grade)}")

    missing = get_missing_components(period_data)
    if missing:
        print("Missing components: " + ", ".join(missing))


def display_individual(student_id=None):
    """Display one student's detailed results across all three periods."""
    if student_id is None:
        student_id = input("Student ID: ").strip()

    student = find_student(student_id)
    if student is None:
        print("Student not found.")
        return

    print_header("STUDENT GRADE REPORT")
    print(f"Student ID: {student[0]}")
    print(f"Name: {student[1]}")

    for period in PERIODS:
        display_period_section(student, period)

    period_grades = calculate_all_period_grades(student)
    final_grade = calc_final_grade(student[2])

    print_header("OVERALL RESULT")
    for period in PERIODS:
        grade = period_grades[period]
        print(
            f"{period} Grade: {format_percentage(grade)} "
            f"| Academic Status: {get_academic_status(grade)}"
        )
    print(f"Final Grade: {format_percentage(final_grade)}")
    print(f"Academic Status: {get_academic_status(final_grade)}")

    missing_periods = [
        period for period in PERIODS
        if calc_period_grade(student[2][period], period) is None
    ]
    if missing_periods:
        print("Incomplete periods: " + ", ".join(missing_periods))


def display_student_directory():
    """Display student IDs and names for teacher reference."""
    print_header("STUDENT LIST")
    print(f"{'No.':<5}{'Student ID':<16}Name")
    print(THIN_SEPARATOR)

    for number, student in enumerate(students, start=1):
        print(f"{number:<5}{student[0]:<16}{student[1]}")


def display_all_students():
    """Display a summary of period grades, final grades, and status for all students."""
    print_header("ALL STUDENTS — GRADE SUMMARY")
    print(
        f"{'Student ID':<13}{'Name':<26}{'P1':>12}{'P2':>12}"
        f"{'P3':>12}{'Final':>12}{'Status':>14}"
    )
    print(THIN_SEPARATOR)

    for student in students:
        period_grades = calculate_all_period_grades(student)
        final_grade = calc_final_grade(student[2])
        status = get_academic_status(final_grade)
        print(
            f"{student[0]:<13}{student[1][:25]:<26}"
            f"{format_grade(period_grades['P1']):>12}"
            f"{format_grade(period_grades['P2']):>12}"
            f"{format_grade(period_grades['P3']):>12}"
            f"{format_grade(final_grade):>12}{status:>14}"
        )


def teacher_login():
    """Authenticate the teacher and return the teacher record."""
    while True:
        print_header("TEACHER LOGIN")
        teacher_id = input("Teacher ID: ").strip()
        password = input("Password: ").strip()
        teacher = find_user(teacher_id, password, "teacher")

        if teacher is not None:
            print(f"Welcome, {teacher[3]}!")
            display_student_directory()
            return teacher

        print("Invalid Teacher ID or password.")
        retry_choice = get_valid_choice(
            "[1] Try Again\n[2] Return to Main Menu\nSelect an option: ",
            1,
            2,
        )
        if retry_choice == 2:
            return None


def teacher_menu():
    """Display teacher actions."""
    while True:
        print_header("TEACHER MENU")
        print("[1] Enter Grades")
        print("[2] Display All Students")
        print("[3] View Individual Student Result")
        print("[4] Logout")

        choice = get_valid_choice("Select an option: ", 1, 4)
        if choice == 1:
            enter_period_grades()
        elif choice == 2:
            display_all_students()
        elif choice == 3:
            display_individual()
        else:
            print("Teacher logged out.")
            return


def student_login():
    """Authenticate a student and return the matching student record."""
    while True:
        print_header("STUDENT LOGIN")
        student_id = input("Student ID: ").strip()
        password = input("Password: ").strip()
        user = find_user(student_id, password, "student")

        if user is not None:
            student = find_student(student_id)
            print(f"Welcome, {student[1]}!")
            return student

        print("Invalid Student ID or password.")
        retry_choice = get_valid_choice(
            "[1] Try Again\n[2] Return to Main Menu\nSelect an option: ",
            1,
            2,
        )
        if retry_choice == 2:
            return None


def student_menu(student):
    """Allow a student to view their own grades without editing them."""
    while True:
        print_header("STUDENT MENU")
        print(f"Student ID: {student[0]}")
        print(f"Name: {student[1]}")
        print("[1] View My Grades")
        print("[2] Logout")

        choice = get_valid_choice("Select an option: ", 1, 2)
        if choice == 1:
            display_individual(student[0])
        else:
            print("Student logged out.")
            return


def main_menu():
    """Display the main menu and route users by role."""
    while True:
        print_header("EDUSENSE — STUDENT GRADE CALCULATOR")
        print("[1] Teacher Login")
        print("[2] Student Login")
        print("[3] Exit")

        choice = get_valid_choice("Select an option: ", 1, 3)
        if choice == 1:
            teacher = teacher_login()
            if teacher is not None:
                teacher_menu()
        elif choice == 2:
            student = student_login()
            if student is not None:
                student_menu(student)
        else:
            print("Thank you for using EduSense!")
            break


if __name__ == "__main__":
    print_header("EDUSENSE — STUDENT GRADE CALCULATOR")
    print(f"Passing Grade: {PASSING_GRADE}%")
    print("Maximum scores per activity: Attendance 3 | Let's Practice 3 | Reflection 3 | Wrap-up Quiz 7 | Check-in Project 100")
    print("Weights: Attendance 5% | Let's Practice 35% | Reflection 15% | Wrap-up Quiz 15% | Check-in Project 30%")
    print("P1: Modules 1-4 | P2: Modules 5-9 | P3: Modules 10-14")
    print("Required activities (Attendance / Practice / Reflection / Quiz / Project):")
    print("P1: 8 / 4 / 4 / 4 / 1 | P2: 10 / 5 / 5 / 5 / 1 | P3: 10 / 5 / 5 / 5 / 1")
    print("Blank entries are allowed; entered scores are calculated against all required activities.")
    print("Final Grade: Average of P1, P2, and P3")
    print("Note: Grade data is held in memory and resets when the program closes.")
    main_menu()
