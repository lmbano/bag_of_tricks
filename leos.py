import time
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def main():
    # Your main code goes here
    result1 = add(1, 2)
    result2 = subtract(5, 3)

    print(f"Addition result: {result1}")
    print(f"Subtraction result: {result2}")
    print(f"Grade old results:", calc_grade_old(90))
    print(f"Grade Optimised results:", calculate_grade(80))

def calculate_grade(score):
    # https://emojipedia.org/chess-pawn
    print("♟️" * 721)
    time.sleep(1)
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    if score >= 50: return "E"


def calc_grade_old(score):
    if score >= 90:
        grade = ("A")
    else:
        if score >= 80:
            grade = ("B")
        else:
            if score >= 70:
                grade = "c"
            else:
                if score >= 60:
                    grade = "D"
                else:
                    grade = "F"
    return grade


if __name__ == "__main__":
    main()
