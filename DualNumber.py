from numbers import Number
from math import log
import math as rmath


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

    def __div(self, other, self_numerator=True):
        if self_numerator and isinstance(other, DualNumber):
            if other.real == 0:
                raise ZeroDivisionError("Division by 0")
            else:
                real = self.real/other.real
                dual = -1*(self.dual*other.real - self.real*other.dual)/(other.real*other.real)
                return DualNumber(real, dual)
        elif self_numerator and isinstance(other, Number):
            if other == 0:
                raise ZeroDivisionError("Division by 0")
            else:
                return DualNumber(self.real/other, self.dual/other)
        elif not self_numerator and isinstance(other, Number):
            if self.real == 0:
                raise ZeroDivisionError("Division by 0")
            else:
                return DualNumber(other / self.real, -1 * (other * self.dual) / self.real ** 2)
        else:
            raise TypeError("Unsupported Type for __div__")

    def __truediv__(self, other):
        return self.__div(other)

    def __rtruediv__(self, other):
        return self.__div(other, self_numerator=False)

    def _pow(self, other, self_base=True):
        if self_base and isinstance(other, Number):
            return DualNumber(self.real ** other, self.dual * other * (self.real ** (other - 1)))
        elif self_base and isinstance(other, DualNumber):
            new_real = self.real ** other.real
            new_dual = (self.real ** (other.real - 1)) * (
                        self.real * other.dual * log(self.real) + other.real * self.dual)
            return DualNumber(new_real, new_dual)
        elif not self_base and isinstance(other, Number):
            return DualNumber(other ** self.real, (other ** self.real) * self.dual * log(other))
        else:
            raise TypeError("Unsupported Type for __pow__")

    def sin(x):
        if isinstance(x, DualNumber):
            return DualNumber(rmath.sin(x.real), rmath.cos(x.real) * x.dual)
        else:
            return rmath.sin(x)


    def __pow__(self, other):
        return self._pow(other)

    def __rpow__(self, other):
        return self._pow(other, self_base=False)

    def __repr__(self):
        return "%s %s %sɛ" % (self.real, '+' if self.dual > 0 else '-', abs(self.dual))


if __name__ == '__main__':
    x = DualNumber(9,10)
    y = DualNumber(11, 10)
    print(x+y)
    print(x/y)
    print(x*y)
    print(x**y)