def validateTopTeamsNumber(number):
    if number < 1:
        raise ValueError("Number can't be less than 1")
    if number > 25:
        raise ValueError("Number can't be more than 25")


def validateNumberIsPositive(number):
    if number < 1:
        raise ValueError("Number has to be positive")
