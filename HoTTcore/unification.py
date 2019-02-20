from HoTTcore.infrastructure import *

"""Constraints are represented with a tuple (lhs,rhs)."""


def equation2str(equation):
    return str(equation[0]) + " == " + str(equation[1])


class UnificationException(Exception):
    pass


class OccursCheckException(UnificationException):
    def __init__(self, equation):
        self.equation = equation

    def __str__(self):
        return "Occurs Check failed: " + equation2str(self.equation)


class ConflictException(UnificationException):
    def __init__(self, equation):
        self.equation = equation

    def __str__(self):
        return "Conflicting equation: " + equation2str(self.equation)


def substitute(constraints, var, subs):
    return [(l.substitute(var, subs), r.substitute(var, subs)) for l, r in constraints]


def unify(constraints, verbose=False):
    # This algorithm comes from
    # https://en.wikipedia.org/wiki/Unification_(computer_science)#A_unification_algorithm
    solutions = []
    while constraints:
        c = constraints.pop()
        if verbose:
            print("Current Equations State:\n" + "\n".join([equation2str(e) for e in constraints]) \
                  + "\n+++++++++++++++++++\n" + equation2str(c) + "\n")
        if c[0] == c[1]:  # DELETE
            pass
        elif isinstance(c[0], Function) and isinstance(c[1], Function):
            if c[0].constructor == c[1].constructor:  # DECOMPOSE
                constraints.extend(zip(c[0].args, c[1].args))
            else:  # CONFLICT
                return ConflictException(c)
        elif isinstance(c[0], Function) and isinstance(c[1], Variable):  # SWAP
            constraints.append((c[1], c[0]))
        elif isinstance(c[1], Function) and isinstance(c[0], Variable):
            if c[0] not in c[1].variables():  # ELIMINATE
                constraints = substitute(constraints, c[0], c[1])
                # constraints.insert(0, c)
                solutions.append(c)
            else:  # OCCURS CHECK
                raise OccursCheckException(c)
    return solutions


if __name__ == "__main__":
    f = Constructor("f", 1)
    c = Constructor("c", 0)
    g = Constructor("g", 2)
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

    expr = g(f(x), g(c(), y))
    eqs = [(expr, z), (f(y), f(g(x, c())))]
    sl = unify(eqs, True)
    print(sl)
    print()

    eqs = [(x, y), (y, f(x))]
    sl = unify(eqs, True)
    print(sl)
