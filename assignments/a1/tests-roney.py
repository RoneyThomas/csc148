from survey import MultipleChoiceQuestion, NumericQuestion, YesNoQuestion, \
    CheckboxQuestion, Answer
from course import Student, Course, sort_students
from criterion import LonelyMemberCriterion, HomogeneousCriterion, \
    HeterogeneousCriterion
from grouper import slice_list, windows, Group, Grouping, AlphaGrouper, RandomGrouper
from survey import Survey
import random
import string
import pytest


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
    assert student_2.get_answer(mcq_1) == None


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

    nq_1 = NumericQuestion(1, "A n.o between 1 and 5", 1, 5)
    nq_1_ans = Answer(1)
    nq_2_ans = Answer(2)
    nq_3_ans = Answer(3)
    nq_4_ans = Answer(5)
    nq_5_ans = Answer(10)
    nq_6_ans = Answer(1)
    assert nq_1.validate_answer(nq_1_ans)
    assert nq_1.validate_answer(nq_2_ans)
    assert nq_1.validate_answer(nq_3_ans)
    assert nq_1.validate_answer(nq_4_ans)
    assert not nq_1.validate_answer(nq_5_ans)
    assert nq_1_ans.is_valid(nq_1)
    assert nq_2_ans.is_valid(nq_1)
    assert nq_3_ans.is_valid(nq_1)
    assert nq_4_ans.is_valid(nq_1)
    assert not nq_5_ans.is_valid(nq_1)
    assert nq_1.get_similarity(nq_1_ans, nq_6_ans) == 1.0
    assert nq_1.get_similarity(nq_1_ans, nq_4_ans) == 0.0
    assert nq_1.get_similarity(nq_2_ans, nq_3_ans) == 0.75

    ynq = YesNoQuestion(1, "Is earth round")
    ynq_1 = Answer(True)
    ynq_2 = Answer(False)
    ynq_3 = Answer(False)
    assert ynq_1.is_valid(ynq)
    assert ynq_2.is_valid(ynq)
    assert not ynq.get_similarity(ynq_1, ynq_2)
    assert ynq.get_similarity(ynq_2, ynq_3)

    cbq = CheckboxQuestion(1, "Cities in Canada",
                           ["Toronto", "Ottawa", "Vancouver"])
    cbq_1 = Answer(["Toronto", "Ottawa"])
    cbq_2 = Answer(["Seoul", "Busan"])
    cbq_3 = Answer(["Toronto", "Ottawa"])
    cbq_4 = Answer(["Toronto", "Vancouver"])
    assert cbq.validate_answer(cbq_1)
    assert not cbq.validate_answer(cbq_2)
    assert cbq_1.is_valid(cbq)
    assert not cbq_2.is_valid(cbq)
    assert cbq.get_similarity(cbq_1, cbq_3) == 1
    assert cbq.get_similarity(cbq_1, cbq_4) == 1 / 3
    assert cbq.get_similarity(cbq_1, cbq_2) == 0.0


def test_course() -> None:
    course_0 = Course("Snake")
    course_0.enroll_students([Student(0, "Tim")])
    course_0.enroll_students([Student(0, "Tim")])
    course_0.enroll_students([Student(0, "Tim"), Student(0, "Roney")])
    assert len(course_0.get_students()) == 1
    course_0.enroll_students([Student(1, "Tim"), Student(2, "Roney")])
    assert len(course_0.get_students()) == 3
    course_1 = Course("Python")
    students = []
    for x in range(10):
        students.append(Student(x, ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6))))
    course_1.enroll_students(students)
    assert len(course_1.get_students()) == len(students)
    assert tuple(sort_students(students, "id")) == course_1.get_students()


def test_criterion() -> None:
    ho_crit = HomogeneousCriterion()
    he_crit = HeterogeneousCriterion()
    lo_crit = LonelyMemberCriterion()

    ynq = YesNoQuestion(1, "Is earth round")
    ynq_1_answers = [Answer(True), Answer(True), Answer(True), Answer(True)]
    ynq_2_answers = [Answer(True), Answer(False), Answer(True), Answer(False)]
    ynq_3_answers = [Answer(True)]
    ynq_4_answers = [Answer(True), Answer(False)]

    assert ho_crit.score_answers(ynq, ynq_1_answers) == 1
    assert ho_crit.score_answers(ynq, ynq_2_answers) == 1 / 3
    assert ho_crit.score_answers(ynq, ynq_3_answers) == 1
    assert ho_crit.score_answers(ynq, ynq_4_answers) == 0

    assert he_crit.score_answers(ynq, ynq_1_answers) == 0.0
    assert he_crit.score_answers(ynq, ynq_2_answers) == pytest.approx(2 / 3,
                                                                      rel=1e-3)
    assert he_crit.score_answers(ynq, ynq_3_answers) == 0.0
    assert he_crit.score_answers(ynq, ynq_4_answers) == 1

    assert lo_crit.score_answers(ynq, ynq_1_answers) == 1
    assert lo_crit.score_answers(ynq, ynq_2_answers) == 0.0
    assert lo_crit.score_answers(ynq, ynq_3_answers) == 1
    assert lo_crit.score_answers(ynq, ynq_4_answers) == 0


def test_grouper() -> None:
    assert windows([3, 4, 6, 2, 3], 2) == [[3, 4], [4, 6], [6, 2], [2, 3]]
    assert windows(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [1, 6.0, False]]
    assert slice_list([3, 4, 6, 2, 3], 2) == [[3, 4], [6, 2], [3]]
    assert slice_list(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [False]]

    g = Group([Student(1, "roney"), Student(2, "tim"), Student(3, "allen")])
    g_1 = Group([Student(1, "roney"), Student(2, "tim"), Student(3, "allen")])
    g_2 = Group([Student(5, "roney"), Student(6, "tim"), Student(7, "allen")])
    assert len(g) == 3
    assert Student(1, "roney") in g
    assert "roney" in str(g)
    gr = Grouping()
    assert gr.add_group(g)
    assert not gr.add_group(g_1)
    assert gr.add_group(g_2)
    assert len(gr) == 2

    course_0 = Course("Snake")
    course_0.enroll_students([Student(1, "a"), Student(2, "b"), Student(3, "c")])
    s = Survey([YesNoQuestion(1, "Is earth round")])
    ag = AlphaGrouper(2)
    gr = ag.make_grouping(course_0, s)
    assert len(gr) == 2

    course_0 = Course("Snake")
    course_0.enroll_students([Student(1, "a"), Student(2, "b"), Student(3, "c")])
    s = Survey([YesNoQuestion(1, "Is earth round")])
    ag = AlphaGrouper(3)
    gr = ag.make_grouping(course_0, s)
    assert len(gr) == 1

    course_0 = Course("Snake")
    course_0.enroll_students([Student(1, "a"), Student(2, "b"), Student(3, "c")])
    s = Survey([YesNoQuestion(1, "Is earth round")])
    ag = RandomGrouper(2)
    gr = ag.make_grouping(course_0, s)
    assert len(gr) == 2

    course_0 = Course("Snake")
    course_0.enroll_students([Student(1, "a"), Student(2, "b"), Student(3, "c")])
    s = Survey([YesNoQuestion(1, "Is earth round")])
    ag = RandomGrouper(3)
    gr = ag.make_grouping(course_0, s)
    assert len(gr) == 1





if __name__ == '__main__':
    pytest.main(['tests-roney.py'])
