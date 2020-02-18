from survey import MultipleChoiceQuestion, Answer
from course import Student, Course, sort_students
import random
import string


def test_student() -> None:
    student_1 = Student(1, "roney")
    student_2 = Student(2, "tim")
    student_3 = Student(3, "allen")
    assert str(student_1) == "roney"
    assert str(student_2) == "tim"
    assert str(student_3) != "roney"
    assert student_1.id == 1
    assert student_2.id != 4
    assert student_3.id == 3
    mcq_1 = MultipleChoiceQuestion(1, "Cities in Canada",
                                   ["Toronto", "Ottawa", "Vancouver"])
    mcq_2 = MultipleChoiceQuestion(2, "C", ["A", "O", "V"])
    mcq_1_ans = Answer("Toronto")
    student_1.set_answer(mcq_1, mcq_1_ans)
    assert student_1.has_answer(mcq_1)
    assert not student_1.has_answer(mcq_2)
    assert student_1.get_answer(mcq_1) == mcq_1_ans
    assert student_1.get_answer(mcq_2) == None


def test_questions() -> None:
    mcq_1 = MultipleChoiceQuestion(1, "Cities in Canada",
                                   ["Toronto", "Ottawa", "Vancouver"])
    assert mcq_1.id == 1
    assert mcq_1.text == "Cities in Canada"
    assert "Cities in Canada" in str(mcq_1)
    assert "Toronto" in str(mcq_1)
    assert "Ottawa" in str(mcq_1)
    assert "Montreal" not in str(mcq_1)
    mcq_1_ans = Answer("Toronto")
    mcq_1_c_ans = Answer("Toronto")
    mcq_2_ans = Answer("Montreal")
    mcq_3_ans = Answer("")
    assert mcq_1_ans.is_valid(mcq_1)
    assert not mcq_2_ans.is_valid(mcq_1)
    assert mcq_1.validate_answer(mcq_1_ans)
    assert not mcq_1.validate_answer(mcq_2_ans)
    assert not mcq_1.validate_answer(mcq_3_ans)
    assert mcq_1.get_similarity(mcq_1_ans, mcq_1_c_ans) == 1.0
    assert mcq_1.get_similarity(mcq_1_ans, mcq_2_ans) == 0.0


def test_course() -> None:
    course_0 = Course("Snake")
    course_0.enroll_students([Student(0, "Tim")])
    course_0.enroll_students([Student(0, "Tim")])
    course_0.enroll_students([Student(0, "Tim"), Student(0, "Tim")])
    assert len(course_0.get_students()) == 1
    course_1 = Course("Python")
    students = []
    for x in range(10):
        students.append(Student(x, ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6))))
    course_1.enroll_students(students)
    assert len(course_1.get_students()) == len(students)
    assert tuple(sort_students(students, "id")) == course_1.get_students()


if __name__ == '__main__':
    import pytest

    pytest.main(['tests-roney.py'])
