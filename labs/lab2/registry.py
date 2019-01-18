from enum import Enum


class SpeedCategory(Enum):
    under_20, under_30, under_40, over_40 = range(4)


class Runner:
    """
    A class representing a runner
    """
    _name: str
    _email: str
    _speed: SpeedCategory

    def __init__(self, name: str, email: str, speed: SpeedCategory):
        """

        :param name: name of the runner
        :param email: email of the runner
        :param speed: speed category of the runner

        Creating a Runner:
        >>> r = Runner('Tim', 't@gmail.com', SpeedCategory.under_20)
        >>> r.name
        'Tim'
        >>> r.email
        't@gmail.com'
        >>> r.speed
        <SpeedCategory.under_20: 0>
        """
        self._name = name
        self._email = email
        self._speed = speed

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def speed(self) -> SpeedCategory:
        return self._speed

    def update_email(self, email: str) -> None:
        """
        Update a runners email

        :param email: new email
         Updating email:
        >>> r = Runner('Tim', 't@gmail.com', SpeedCategory.under_20)
        >>> r.email
        't@gmail.com'
        >>> r.update_email('m@gmail.com')
        >>> r.email
        'm@gmail.com'
        """
        self._email = email

    def update_speed(self, speed) -> None:
        """

        Update speed category of runner
        :param speed: Speed category

        Updating speed category
        >>> r = Runner('Tim', 't@gmail.com', SpeedCategory.under_20)
        >>> r.speed
        <SpeedCategory.under_20: 0>
        >>> r.update_speed(SpeedCategory.under_40)
        >>> r.speed
        <SpeedCategory.under_40: 2>
        """
        self._speed = speed


class Registry:
    """
    A registry holding race info
    """
    runners: [Runner] = []

    def register(self, name: str, email: str, speed: SpeedCategory) -> None:
        """

        :param name: name of the runner
        :param email: email of the runner
        :param speed: speed category of the runner

        >>> r = Registry()
        >>> r.register('Tim', 't@gmail.com', SpeedCategory.under_20)
        >>> r.runners[0].name
        'Tim'
        >>> r.runners[0].email
        't@gmail.com'
        >>> r.runners[0].speed
        <SpeedCategory.under_20: 0>
        """
        runner = Runner(name, email, speed)
        self.runners.append(runner)

    def get_speed_runners(self, speed: SpeedCategory) -> list:
        """

        :param speed: speed category

        >>> r = Registry()
        >>> r.register('Tim', 't@gmail.com', SpeedCategory.under_20)
        >>> less_than_zero = r.get_speed_runners(SpeedCategory.under_20)
        >>> less_than_zero
        dsf
        """
        less_than_zero = list(filter(lambda runner: runner.speed == speed, self.runners))
        return less_than_zero[0]

    # def __del__(self, email: str):
    #     print("this is working")
    #     for index, runner in enumerate(self.runners):
    #         if runner.email == email:
    #             del self.runners[index]
    #             break

    def delete_runner(self, email: str) -> None:
        for index, runner in enumerate(self.runners):
            if runner.email == email:
                del self.runners[index]
                break


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # Optionally, check your work with python_ta!
    # import python_ta
    #
    # python_ta.check_all(config={'extra-imports': ['Enum']})
