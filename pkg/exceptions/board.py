from pkg.exceptions import UserDefinedException


class BoardDimensionsException(UserDefinedException):
    pass


class BoardIndexOutOfBounds(UserDefinedException):
    pass
