from numbers import Number


class DualNumber:
    def __init__(self, real, dual):
        self.real = real
        self.dual = dual
    def __add__(self, other):
        if isinstance(other, DualNumber):
            return DualNumber(self.real+other.real, self.dual+other.dual)
        elif isinstance(other, Number):
            return DualNumber(self.real+other, self.dual)
        else:
            raise TypeError("Unsupported Type for __add__")
    def __radd__(self, other):
        return DualNumber(self.real+other, self.dual)

    def _sub(self, other, self_first=True):
        if self_first and isinstance(other, DualNumber):
            return DualNumber(self.real - other.real, self.dual - other.dual)
        elif self_first and isinstance(other, Number):
            return DualNumber(self.real - other, self.dual)
        elif not self_first and isinstance(other, Number):
            return DualNumber(other - self.real, -1 * self.dual)
        else:
            raise TypeError("Unsupported Type for __sub__")

    def __sub__(self, other):
        return self._sub(other)

    def __rsub__(self, other):
        return self._sub(other, self_first=False)

    def __mul(self, other):
        if isinstance(other, DualNumber):
            return DualNumber(self.real * other.real, self.real*other.dual+other.real*self.dual)
        elif isinstance(other, Number):
            return DualNumber(self.real * other,  self.dual * other)
        else:
            raise TypeError("Unsupported Type for __add__")

    def __mul__(self, other):
        return self.__mul(other)

    def __rmul__(self, other):
        return self.__mul(other)


if __name__ == '__main__':
    x = DualNumber(9,10)
    y = DualNumber(11, 10)
    print(x+y)
    print(x+1)
    print(4+y)