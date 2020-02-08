from datetime import datetime
from gym import WorkoutClass, Instructor, Gym


def test_workout() -> None:
    workout_class = WorkoutClass('Running',
                                 ['Strength Training', 'Interval Training'])
    assert workout_class.get_name() == 'Running'
    assert len(workout_class.get_required_certificates()) == 2


def test_instructor() -> None:
    instructor = Instructor(1, 'Tim Apple')
    assert instructor.name == 'Tim Apple'
    assert instructor.get_id() == 1
    assert instructor.get_num_certificates() == 0
    workout_class = WorkoutClass('Running',
                                 ['Strength Training', 'Interval Training'])
    assert instructor.can_teach(workout_class) is False
    instructor.add_certificate('Strength Training')
    assert instructor.can_teach(workout_class) is False
    instructor.add_certificate('Interval Training')
    assert instructor.can_teach(workout_class) is True
    assert instructor.get_num_certificates() == 2


def test_gym() -> None:
    gc = Gym("Gold Ring")
    assert gc.name == "Gold Ring"
    assert gc._instructors == {}
    assert gc._workouts == {}
    assert gc._rooms == {}
    assert gc._schedule == {}
    diane = Instructor(1, 'Diane')
    assert gc.add_instructor(diane) is True
    assert gc.add_instructor(diane) is False
    workout_class_run = WorkoutClass('Running',
                                     ['Strength Training', 'Interval Training',
                                      'Long Runs', 'Tempo', 'FTP Test'])
    workout_class_cycling = WorkoutClass('Cycling Basics',
                                         ['Strength Training',
                                          'Interval Training', 'Tempo'])
    assert gc.add_workout_class(workout_class_run) is True
    assert gc.add_workout_class(workout_class_run) is False
    assert gc.add_workout_class(workout_class_cycling) is True
    assert gc.add_room('Cycling Room', 100) is True
    assert gc.add_room('Strength Room', 100) is True
    assert gc.add_room('Strength Room', 200) is False
    assert len(gc._instructors) == 1
    assert len(gc._workouts) == 2
    assert len(gc._rooms) == 2
    # Testing if we can schedule a workout when the instructor is not qualified
    JAN_27_2020 = datetime(2020, 1, 27, 12, 0)
    assert gc.schedule_workout_class(JAN_27_2020, 'Strength Room',
                                     workout_class_run.get_name(),
                                     diane.get_id()) is False
    diane.add_certificate('Strength Training')
    diane.add_certificate('Interval Training')
    diane.add_certificate('Long Runs')
    diane.add_certificate('Tempo')
    diane.add_certificate('FTP Test')
    # Testing if we can schedule when the instructor is qualified
    assert gc.schedule_workout_class(JAN_27_2020, 'Strength Room',
                                     workout_class_run.get_name(),
                                     diane.get_id()) is True
    # Testing if we can schedule when the instructor who is already scheduled
    assert gc.schedule_workout_class(JAN_27_2020, 'Strength Room',
                                     workout_class_run.get_name(),
                                     diane.get_id()) is False
    # Trying to add an offering when the instructor is not available
    assert gc.schedule_workout_class(JAN_27_2020, 'Cycling Room',
                                     workout_class_cycling.get_name(),
                                     diane.get_id()) is False


def test_register() -> None:
    gc = Gym("Gold Ring")
    diane = Instructor(1, 'Diane')
    roney = Instructor(2, 'Roney')
    workout_class_run = WorkoutClass('Running',
                                     ['Strength Training', 'Interval Training',
                                      'Long Runs', 'Tempo', 'FTP Test'])
    workout_class_cycling = WorkoutClass('Cycling Basics',
                                         ['Strength Training',
                                          'Interval Training', 'Tempo'])
    gc.add_workout_class(workout_class_run)
    gc.add_workout_class(workout_class_cycling)
    gc.add_instructor(diane)
    gc.add_instructor(roney)
    JAN_27_2020 = datetime(2020, 1, 27, 12, 0)
    gc.add_room('Cycling Room', 1)
    gc.add_room('Strength Room', 1)
    gc.schedule_workout_class(JAN_27_2020, 'Strength Room',
                              workout_class_run.get_name(),
                              diane.get_id())
    gc.schedule_workout_class(JAN_27_2020, 'Cycling Room',
                              workout_class_cycling.get_name(),
                              roney.get_id())
    # Testing if we can register a new client,
    # if the instructor is not qualified
    assert gc.register(JAN_27_2020, 'Philip', 'Running') is False
    diane.add_certificate('Strength Training')
    diane.add_certificate('Interval Training')
    diane.add_certificate('Long Runs')
    diane.add_certificate('Tempo')
    diane.add_certificate('FTP Test')
    gc.schedule_workout_class(JAN_27_2020, 'Strength Room',
                              workout_class_run.get_name(),
                              diane.get_id())
    assert gc.register(JAN_27_2020, 'Philip', 'Running') is True
    # Testing if we can register a already registered client
    assert gc.register(JAN_27_2020, 'Philip', 'Running') is False
    # Testing if we can register a already registered client to different class
    assert gc.register(JAN_27_2020, 'Philip', 'Cycling Basics') is False
    # Testing if we can register to already full class
    assert gc.register(JAN_27_2020, 'Roth', 'Running') is False
    assert gc.register(JAN_27_2020, 'Roth', 'Cycling Basics') is False


def test_offerings_at():
    gc = Gym("Gold Ring")
    diane = Instructor(1, 'Diane')
    roney = Instructor(2, 'Roney')
    diane.add_certificate('Strength Training')
    diane.add_certificate('Interval Training')
    diane.add_certificate('Long Runs')
    diane.add_certificate('Tempo')
    diane.add_certificate('FTP Test')
    roney.add_certificate('Strength Training')
    roney.add_certificate('Interval Training')
    roney.add_certificate('Tempo')
    workout_class_run = WorkoutClass('Running',
                                     ['Strength Training', 'Interval Training',
                                      'Long Runs', 'Tempo', 'FTP Test'])
    workout_class_cycling = WorkoutClass('Cycling Basics',
                                         ['Strength Training',
                                          'Interval Training', 'Tempo'])
    gc.add_workout_class(workout_class_run)
    gc.add_workout_class(workout_class_cycling)
    gc.add_instructor(diane)
    gc.add_instructor(roney)
    JAN_27_2020 = datetime(2020, 1, 27, 12, 0)
    gc.add_room('Cycling Room', 1)
    gc.add_room('Strength Room', 1)
    gc.schedule_workout_class(JAN_27_2020, 'Strength Room',
                              workout_class_run.get_name(),
                              diane.get_id())
    gc.schedule_workout_class(JAN_27_2020, 'Cycling Room',
                              workout_class_cycling.get_name(),
                              roney.get_id())
    assert ('Diane', 'Running', 'Strength Room') in gc.offerings_at(JAN_27_2020)
    assert len(gc.offerings_at(JAN_27_2020)) == 2
    assert len(gc.offerings_at(datetime(2020, 1, 28, 12, 0))) == 0


def test_instructor_hours():
    gc = Gym("Gold Ring")
    diane = Instructor(1, 'Diane')
    roney = Instructor(2, 'Roney')
    diane.add_certificate('Strength Training')
    diane.add_certificate('Interval Training')
    diane.add_certificate('Long Runs')
    diane.add_certificate('Tempo')
    diane.add_certificate('FTP Test')
    roney.add_certificate('Strength Training')
    roney.add_certificate('Interval Training')
    roney.add_certificate('Tempo')
    workout_class_run = WorkoutClass('Running',
                                     ['Strength Training', 'Interval Training',
                                      'Long Runs', 'Tempo', 'FTP Test'])
    workout_class_cycling = WorkoutClass('Cycling Basics',
                                         ['Strength Training',
                                          'Interval Training', 'Tempo'])
    gc.add_workout_class(workout_class_run)
    gc.add_workout_class(workout_class_cycling)
    gc.add_instructor(diane)
    gc.add_instructor(roney)
    JAN_27_2020 = datetime(2020, 1, 27, 12, 0)
    JAN_28_2020 = datetime(2020, 1, 28, 12, 0)
    assert gc.instructor_hours(JAN_27_2020, JAN_28_2020) == {1: 0, 2: 0}
    gc.add_room('Cycling Room', 1)
    gc.add_room('Strength Room', 1)
    gc.schedule_workout_class(JAN_27_2020, 'Strength Room',
                              workout_class_run.get_name(),
                              diane.get_id())
    gc.schedule_workout_class(JAN_27_2020, 'Cycling Room',
                              workout_class_cycling.get_name(),
                              roney.get_id())
    assert gc.instructor_hours(JAN_27_2020, JAN_28_2020) == {1: 1, 2: 1}
    gc.schedule_workout_class(JAN_28_2020, 'Strength Room',
                              workout_class_run.get_name(),
                              diane.get_id())
    assert gc.instructor_hours(JAN_27_2020, JAN_28_2020) == {1: 2, 2: 1}


def test_payroll():
    gc = Gym("Gold Ring")
    diane = Instructor(1, 'Diane')
    roney = Instructor(2, 'Roney')
    diane.add_certificate('Strength Training')
    diane.add_certificate('Interval Training')
    diane.add_certificate('Long Runs')
    diane.add_certificate('Tempo')
    diane.add_certificate('FTP Test')
    roney.add_certificate('Strength Training')
    roney.add_certificate('Interval Training')
    roney.add_certificate('Tempo')
    workout_class_run = WorkoutClass('Running',
                                     ['Strength Training', 'Interval Training',
                                      'Long Runs', 'Tempo', 'FTP Test'])
    workout_class_cycling = WorkoutClass('Cycling Basics',
                                         ['Strength Training',
                                          'Interval Training', 'Tempo'])
    gc.add_workout_class(workout_class_run)
    gc.add_workout_class(workout_class_cycling)
    gc.add_instructor(diane)
    gc.add_instructor(roney)
    JAN_27_2020 = datetime(2020, 1, 27, 12, 0)
    JAN_28_2020 = datetime(2020, 1, 28, 12, 0)
    assert gc.instructor_hours(JAN_27_2020, JAN_28_2020) == {1: 0, 2: 0}
    gc.add_room('Cycling Room', 1)
    gc.add_room('Strength Room', 1)
    gc.schedule_workout_class(JAN_27_2020, 'Strength Room',
                              workout_class_run.get_name(),
                              diane.get_id())
    gc.schedule_workout_class(JAN_27_2020, 'Cycling Room',
                              workout_class_cycling.get_name(),
                              roney.get_id())
    assert gc.instructor_hours(JAN_27_2020, JAN_28_2020) == {1: 1, 2: 1}
    gc.schedule_workout_class(JAN_28_2020, 'Strength Room',
                              workout_class_run.get_name(),
                              diane.get_id())
    assert gc.instructor_hours(JAN_27_2020, JAN_28_2020) == {1: 2, 2: 1}
    assert (1, 'Diane', 2, 65.0) in gc.payroll(JAN_27_2020, JAN_28_2020, 25.0)
    assert (2, 'Roney', 1, 29.5) in gc.payroll(JAN_27_2020, JAN_28_2020, 25.0)


if __name__ == '__main__':
    import pytest

    pytest.main(['test_roney.py'])
