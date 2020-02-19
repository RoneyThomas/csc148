import random
import string

from course import Course, Student, sort_students
from survey import Answer, MultipleChoiceQuestion, NumericQuestion
from survey import CheckboxQuestion, YesNoQuestion, Survey
from criterion import  HomogeneousCriterion, HeterogeneousCriterion
from criterion  import LonelyMemberCriterion
import pytest

def test_student() -> None:
    student_1 = Student(1, "roney")
    student_2 = Student(2, "tim")
    student_3 = Student(3, "allen")
    assert str(student_1) == "roney"
    assert str(student_2) == "tim"
    assert str(student_3) != "roney"
    assert student_1.id == 1
    assert student_2.id == 2
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


def test_answers_survey() -> None:
    student_1 = Student(1, "roney")
    student_2 = Student(2, "tim")
    student_3 = Student(3, "allen")
    student_4 = Student(3, "allen")
    assert str(student_1) == "roney"
    assert str(student_2) == "tim"
    assert str(student_3) != "roney"
    assert student_1.id == 1
    assert student_2.id == 2
    assert student_3.id == 3
    mcq_1 = MultipleChoiceQuestion(1, "Cities in Canada",
                                   ["Toronto", "Ottawa", "Vancouver"])
    mcq_2 = MultipleChoiceQuestion(2, "C", ["A", "O", "V"])
    mcq_1_ans = Answer("Toronto")
    student_1.set_answer(mcq_1, mcq_1_ans)
    student_2.set_answer(mcq_1, mcq_1_ans)
    student_3.set_answer(mcq_1, mcq_1_ans)
    lst = [student_1, student_2, student_3, student_4]
    course_0 = Course("Snake")
    assert len(course_0.get_students()) == 0
    course_0.enroll_students(lst)
    lst1 = [student_1, student_2, student_3]
    course_0.enroll_students(lst1)
    assert len(course_0.get_students()) == 3
    for student in course_0.get_students():
        assert student.has_answer(mcq_1)

    survey_ = Survey([mcq_1])
    assert len(survey_) == 1
    assert course_0.all_answered(survey_)

    student_5 = Student(55, "allen")
    course_0.enroll_students([student_5])
    assert not course_0.all_answered(survey_)

    course_0 = Course("Snake")
    student_1 = Student(1, "roney")
    student_2 = Student(2, "tim")
    student_3 = Student(3, "allen")
    student_4 = Student(4, "Sarah")


    q_1 = MultipleChoiceQuestion(1, "Cities in Canada",
                                 ["Toronto", "Ottawa", "Vancouver"])

    q_2 = NumericQuestion(2, "numbers of days in a week", 1, 7)

    q_3 = YesNoQuestion(3, "Are you Happy")

    q_4 = CheckboxQuestion(4, "Q4", ['a', 'b', 'c'])

    q_5 = MultipleChoiceQuestion(5, "C", ["A", "O", "V"])

    q_1_ans = Answer("Toronto")
    q_2_ans = Answer(4)
    q_3_ans = Answer(True)
    q_4_ans = Answer(['a', 'b'])
    q_5_ans = Answer('A')

    survey_ = Survey([q_1, q_2, q_3, q_4, q_5])
    questions = survey_.get_questions()

    lst = [student_1, student_2, student_3, student_4]

    a_lst = [q_1_ans, q_2_ans, q_3_ans, q_4_ans, q_5_ans]

    for students in lst:
        for i, a in enumerate(a_lst):
            students.set_answer(questions[i], a)
    course_0.enroll_students(lst)

    assert course_0.all_answered(survey_)

    for question in survey_.get_questions():
        assert survey_._get_weight(question) == 1
        survey_.set_weight(2, question)
        assert survey_._get_weight(question) == 2
        assert question in survey_
        assert type(survey_._get_criterion(question)) == HomogeneousCriterion

    survey_.set_weight(3, survey_.get_questions()[3])

    assert survey_.score_students(lst) == 2.2

    survey1 = Survey([])
    assert survey1.score_students(lst) == 0


def test_criterion() -> None:
    q = CheckboxQuestion(4, "Q4", ['a', 'b', 'c'])
    a1 = Answer(['a'])
    a2 = Answer(['b'])
    a3 = Answer(['c'])
    a123 = Answer(['csadf'])

    assert a1.is_valid(q)

    a_list = [a1, a1, a1, a1, a1, a1, a1, a1, a2, a2, a2, a2, a2, a3, a3]
    a2_list = [a3, a3]
    a3_list = [a3, a3, a123]
    a4_list = [a3, a3, a1, a2]
    a5_list = [a3]

    ho = HomogeneousCriterion()
    he = HeterogeneousCriterion()
    lo = LonelyMemberCriterion()

    assert lo.score_answers(q, a_list) == 0.0
    assert lo.score_answers(q, a2_list) == 1.0
    assert he.score_answers(q, a4_list) == 0.8333333333333334
    assert he.score_answers(q, a5_list) == 0.0
    assert he.score_answers(q, a5_list) == 0.0
    assert ho.score_answers(q, a_list) == 0.37142857142857144




if __name__ == '__main__':
    import pytest

    pytest.main(['test-lucas.py'])
