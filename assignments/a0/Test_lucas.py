"""CSC148 Assignment 0: Sample tests

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 0.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Mario Badr, Christine Murad, Diane Horton, Misha Schwartz, Sophia Huynh
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Christine Murad, Diane Horton, Misha Schwartz,
Sophia Huynh and Jaisie Sin
"""

from datetime import datetime
from gym import WorkoutClass, Instructor, Gym, load_data #take THIS OUT
ac = load_data('athletic-centre.txt', 'Athletic Centre')


def test_instructor_load_data() -> None:
    date = datetime(2018, 1, 14, 18, 0)
    date1 = datetime(2021, 1, 14, 18, 0)
    assert ac.instructor_hours(date,date1) == {1: 2, 2: 1, 3: 2, 4: 0, 5: 2}


def test_register_load_data() -> None:
    """register one person from load data"""
    jan_14_2020_9_00 = datetime(2020, 1, 14, 9, 0)
    assert ac.register(jan_14_2020_9_00, 'sammy@gmail.com', 'Fit Mix')
    assert ac.register(jan_14_2020_9_00, 'Andrea@gmail.com', 'Fit Mix') is True


def test_instructor_attributes() -> None:
    """Test the public attributes of a new instructor."""
    instructor = Instructor(5, 'Matthew')
    assert instructor.get_id() == 5
    assert instructor.name == 'Matthew'


def test_instructor_one_certificate_get_certificates() -> None:
    """Test Instructor.get_num_certificates with a single certificate."""
    instructor = Instructor(5, 'Matthew')
    assert instructor.add_certificate('Kickboxing')
    assert instructor.get_num_certificates() == 1


def test_instructor_one_certificate_get_no_certificates() -> None:
    """Test Instructor.get_num_certificates with a single certificate."""
    instructor = Instructor(5, 'Matthew')
    assert instructor.get_num_certificates() == 0


def test_instructor_one_certificate_get_multiple_certificates() -> None:
    """Test Instructor.get_num_certificates with 5 certificate."""
    instructor = Instructor(5, 'Matthew')
    assert instructor.add_certificate('a')
    assert instructor.add_certificate('b')
    assert instructor.add_certificate('c')
    assert instructor.add_certificate('d')
    assert instructor.add_certificate('e')
    assert instructor.get_num_certificates() == 5


def test_instructor_get_multi_2f_certificates() -> None:
    """Test Instructor.get_num_certificates with 3T, 2 duplicate
    certificates."""
    instructor = Instructor(5, 'Matthew')
    assert instructor.add_certificate('a')
    instructor.add_certificate('a')
    instructor.add_certificate('a')
    assert instructor.add_certificate('d')
    assert instructor.add_certificate('e')
    assert instructor.get_num_certificates() == 3


def test_gym_add_one_instructor() -> None:
    """Add 1 instructor to the gym"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert ac.add_instructor(diane)


def test_gym_add_two_instructor() -> None:
    """Add 2 different instructors to the gym"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    timmy = Instructor(2, 'Timmy')
    assert ac.add_instructor(diane)
    assert ac.add_instructor(timmy)


def test_gym_add_same_instructor() -> None:
    """Add the same instructor to the gym twice and another new one"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    timmy = Instructor(2, 'Timy')
    assert ac.add_instructor(diane)
    assert ac.add_instructor(diane) is False
    assert ac.add_instructor(timmy)


def test_add_one_workout() -> None:
    """Add one workout to the Gym"""
    ac = Gym('Athletic Centre')
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training'])
    assert ac.add_workout_class(kickboxing)


def test_add_three_workouts() -> None:
    """Add three workouts to the Gym"""
    ac = Gym('Athletic Centre')
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training'])
    a = WorkoutClass('b', ['Strength Training'])
    b = WorkoutClass('c', ['Strength Training'])
    assert ac.add_workout_class(kickboxing)
    assert ac.add_workout_class(a)
    assert ac.add_workout_class(b)


def test_add_three_workouts_one_duplicate() -> None:
    """Add three workouts to the Gym"""
    ac = Gym('Athletic Centre')
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training'])
    a = WorkoutClass('b', ['Strength Training'])
    b = WorkoutClass('c', ['Strength Training'])
    assert ac.add_workout_class(kickboxing)
    assert ac.add_workout_class(a)
    assert ac.add_workout_class(a) is False
    assert ac.add_workout_class(b)


def test_add_5_workouts() -> None:
    """Add three workouts to the Gym"""
    ac = Gym('Athletic Centre')
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training'])
    a = WorkoutClass('b', ['Strength Training'])
    b = WorkoutClass('c', ['Strength Training'])
    d = WorkoutClass('d', ['Strength Training'])
    e = WorkoutClass('e', ['Strength Training'])
    assert ac.add_workout_class(kickboxing)
    assert ac.add_workout_class(a)
    assert ac.add_workout_class(b)
    assert ac.add_workout_class(d)
    a = WorkoutClass('bz', ['Strength Training'])
    assert ac.add_workout_class(e)
    assert ac.add_workout_class(a)
    assert len(ac._workouts) == 6


def test_add_one_room() -> None:
    """add one room to a gym"""
    ac = Gym('Athletic Centre')
    assert ac.add_room('Dance Studio', 50)


def test_add_3_rooms() -> None:
    """add 3 room to a gym"""
    ac = Gym('Athletic Centre')
    assert ac.add_room('Dance Studio', 50)
    assert ac.add_room('Dance a', 50)
    assert ac.add_room('Dance b', 50)
    assert len(ac._rooms) == 3

def test_canteach_1cert_1require() -> None:
    """Test can teach with 1 cert and 1 requirement"""
    matylda = Instructor(1, 'Matylda')
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training'])
    assert matylda.can_teach(kickboxing) is False
    assert matylda.add_certificate('Strength Training')
    assert matylda.can_teach(kickboxing)


def test_canteach_1cert_3require() -> None:
    """Test can teach with 1 cert and 1 requirement"""
    matylda = Instructor(1, 'Matylda')
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training',"a",'B'])
    assert matylda.can_teach(kickboxing) is False
    assert matylda.add_certificate('Strength Training')
    assert matylda.can_teach(kickboxing) is False


def test_canteach_3cert_3require() -> None:
    """Test can teach with 1 cert and 1 requirement"""
    matylda = Instructor(1, 'Matylda')
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training',"a",'B'])
    assert matylda.can_teach(kickboxing) is False
    assert matylda.add_certificate('Strength Training')
    assert matylda.add_certificate('a')
    assert matylda.add_certificate('B')
    assert matylda.can_teach(kickboxing)


def test_canteach_4cert_3require() -> None:
    """Test can teach with 1 cert and 1 requirement"""
    matylda = Instructor(1, 'Matylda')
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training',"a",'B'])
    assert matylda.can_teach(kickboxing) is False
    assert matylda.add_certificate('Strength Training')
    assert matylda.add_certificate('a')
    assert matylda.add_certificate('B')
    assert matylda.add_certificate('fourth')
    assert matylda.can_teach(kickboxing)


def test_add_3_one_repeat_room() -> None:
    """add 3 room to a gym and one replicate"""
    ac = Gym('Athletic Centre')
    assert ac.add_room('Dance Studio', 50)
    assert ac.add_room('Dance a', 50)
    assert ac.add_room('Dance b', 50)
    assert ac.add_room('Dance b', 50) is False
    assert len(ac._rooms) == 3


def test_add_one_workout_schedule() -> None:
    """ Add one workout to the schedule"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert ac.add_instructor(diane)
    assert diane.add_certificate('Cardio 1')
    assert ac.add_room('Dance Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                   boot_camp.get_name(), diane.get_id())


def test_add_three_workout_schedule_diff_time() -> None:
    """ Add three workout to the schedule at different times"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert ac.add_instructor(diane)
    assert diane.add_certificate('Cardio 1')
    assert ac.add_room('Dance Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    sep_9_2020_12_00 = datetime(2020, 9, 9, 12, 0)
    sep_9_2020_1_00 = datetime(2020, 9, 9, 1, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                   boot_camp.get_name(), diane.get_id())
    assert ac.schedule_workout_class(sep_9_2020_12_00, 'Dance Studio',
                                   boot_camp.get_name(), diane.get_id())
    assert ac.schedule_workout_class(sep_9_2020_1_00, 'Dance Studio',
                                     boot_camp.get_name(), diane.get_id())


def test_add_three_workout_schedule_diff_time_unqualified() -> None:
    """ Add three workout to the schedule at different times, but
    instructor unqualified so you can't"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    timmy = Instructor(2, 'Timmy')
    assert ac.add_instructor(diane)
    assert ac.add_instructor(timmy)

    assert timmy.add_certificate('Cardio 1')
    assert ac.add_room('Dance Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    sep_9_2020_12_00 = datetime(2020, 9, 9, 12, 0)
    sep_9_2020_1_00 = datetime(2020, 9, 9, 1, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                   boot_camp.get_name(), diane.get_id()) is False
    assert ac.schedule_workout_class(sep_9_2020_12_00, 'Dance Studio',
                                   boot_camp.get_name(), diane.get_id()) is False
    assert ac.schedule_workout_class(sep_9_2020_1_00, 'Dance Studio',
                                     boot_camp.get_name(),
                                     timmy.get_id())


def test_add_two_workout_schedule_diff_time() -> None:
    """ Add two workout to the schedule at different times"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert ac.add_instructor(diane)
    assert diane.add_certificate('Cardio 1')
    assert ac.add_room('Dance Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    sep_9_2020_12_00 = datetime(2020, 9, 9, 12, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                   boot_camp.get_name(), diane.get_id())
    assert ac.schedule_workout_class(sep_9_2020_12_00, 'Dance Studio',
                                   boot_camp.get_name(), diane.get_id())


def test_add_three_workout_schedule_1_dup_time() -> None:
    """ Add three workout to the schedule, 2 with different rooms
    at the same time, and one with a room at a different time"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    timmy = Instructor(2, 'Timmy')
    assert ac.add_instructor(diane)
    assert ac.add_instructor(timmy)

    assert diane.add_certificate('Cardio 1')
    assert timmy.add_certificate('Cardio 1')

    assert ac.add_room('Dance Studio', 50)
    assert ac.add_room('Bike Studio', 50)

    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)

    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    sep_9_2020_1_00 = datetime(2020, 9, 9, 1, 0)

    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                   boot_camp.get_name(), diane.get_id())

    assert ac.schedule_workout_class(sep_9_2020_1_00, 'Dance Studio',
                                     boot_camp.get_name(), timmy.get_id())

    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Bike Studio',
                                     boot_camp.get_name(), diane.get_id()) is False


def test_add_three_workout_schedule_3_at_same_time() -> None:
    """ Add three different workouts to the schedule at the same time"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    timmy = Instructor(2, 'Timmy')
    greg = Instructor(3, 'Greg')
    assert ac.add_instructor(diane)
    assert ac.add_instructor(timmy)
    assert ac.add_instructor(greg)

    assert diane.add_certificate('Cardio 1')
    assert timmy.add_certificate('Cardio 1')
    assert greg.add_certificate('Cardio 1')

    assert ac.add_room('Dance Studio', 50)
    assert ac.add_room('Bike Studio', 50)
    assert ac.add_room('Lift Studio', 50)

    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)

    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)

    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                     boot_camp.get_name(), diane.get_id())

    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Lift Studio',
                                     boot_camp.get_name(), greg.get_id())

    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Bike Studio',
                                     boot_camp.get_name(), diane.get_id()) is False


def test_register_one_person() -> None:
    """Register one person to one workout class"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert diane.add_certificate('Cardio 1')
    assert ac.add_instructor(diane)
    assert ac.add_room('Dance Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio', \
                                   boot_camp.get_name(), diane.get_id())
    assert ac.register(sep_9_2019_12_00, 'Philip', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 'Tim', 'Boot Camp') is True


def test_register_two_diff_person_diff_room() -> None:
    """Register 2 diff people to same workout class, diff room, same time"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert diane.add_certificate('Cardio 1')
    assert ac.add_instructor(diane)
    assert ac.add_room('Dance Studio', 50)
    assert ac.add_room('Bike Studio', 5)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio', \
                                   boot_camp.get_name(), diane.get_id())
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Bike Studio', \
                                     boot_camp.get_name(), diane.get_id())\
                                     is False
    assert ac.register(sep_9_2019_12_00, 'Greg', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 'Greg', 'Boot Camp') is False
    assert ac.register(sep_9_2019_12_00, 'Tim', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 'Tim', 'Boot Camp') is False


def test_register_over_capacity() -> None:
    """Add too many people to a room"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert diane.add_certificate('Cardio 1')
    assert ac.add_instructor(diane)
    assert ac.add_room('Dance Studio', 1)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio', \
                                     boot_camp.get_name(), diane.get_id())
    assert ac.register(sep_9_2019_12_00, 'Greg', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 'Tim', 'Boot Camp') is False


def test_register_same_person_diff_room() -> None:
    """Register 2 diff people to same workout class, diff room, same time"""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert diane.add_certificate('Cardio 1')
    assert ac.add_instructor(diane)

    timmy = Instructor(2, 'Timmy')
    assert timmy.add_certificate('Cardio 1')
    assert ac.add_instructor(timmy)


    assert ac.add_room('Dance Studio', 1)
    assert ac.add_room('Bike Studio', 1)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    workout_camp = WorkoutClass('workout 1', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    assert ac.add_workout_class(workout_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio', \
                                   boot_camp.get_name(), diane.get_id())
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Bike Studio', \
                                     workout_camp.get_name(), timmy.get_id())
    assert ac.register(sep_9_2019_12_00, 'Greg', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 'Kim', 'workout 1')


def test_instructor_one_certificate_can_teach() -> None:
    """Test Instructor.can_teach with a single satisfying certificate."""
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard'])
    assert instructor.add_certificate('Lifeguard')
    assert instructor.can_teach(swimming)


def test_gym_register_one_class() -> None:
    """Test Gym.register with a single user and class."""
    ac = Gym('Athletic Centre')
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard'])
    jan_28_2020_11_00 = datetime(2020, 1, 29, 11, 0)
    assert instructor.add_certificate('Lifeguard')
    assert ac.add_workout_class(swimming)
    assert ac.add_instructor(instructor)
    assert ac.add_room('25-yard Pool', 100)
    assert ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    assert ac.register(jan_28_2020_11_00, 'Benjamin', 'Swimming')


def test_gym_offerings_at_one_class() -> None:
    ac = Gym('Athletic Centre')
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard'])
    jan_28_2020_11_00 = datetime(2020, 1, 29, 11, 0)
    assert instructor.add_certificate('Lifeguard')
    assert ac.add_workout_class(swimming)
    assert ac.add_instructor(instructor)
    assert ac.add_room('25-yard Pool', 100)
    assert ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    assert ac.offerings_at(jan_28_2020_11_00) == \
        [('Matthew', 'Swimming', '25-yard Pool')]


def test_gym_one_instructor_one_hour_pay_no_certificates() -> None:
    ac = Gym('Athletic Centre')
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', [])
    jan_28_2020_11_00 = datetime(2020, 1, 29, 11, 0)
    assert ac.add_workout_class(swimming)
    assert ac.add_instructor(instructor)
    assert ac.add_room('25-yard Pool', 100)
    assert ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    t1 = datetime(2020, 1, 17, 11, 0)
    t2 = datetime(2020, 1, 29, 13, 0)
    assert ac.payroll(t1, t2, 22.0) == [(5, 'Matthew', 1, 22)]


def test_gym_multiple_instructors_pay_combines_certificates()-> None:
    date = datetime(2018, 1, 14, 18, 0)
    date1 = datetime(2021, 1, 14, 18, 0)
    assert ac.payroll(date, date1, 1) == [(1, 'Diane', 2, 6.5),
                                          (2, 'David', 1, 2.5),
                                          (3, 'Jennifer', 2, 5.0),
                                          (4, 'Michelle', 0, 3.0),
                                          (5, 'Mario Badr', 2, 6.5)]




if __name__ == '__main__':
    import pytest
    pytest.main(['Test_lucas.py'])
