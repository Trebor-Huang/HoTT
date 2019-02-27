from HoTTcore.basic import *
from HoTTcore.ITT import Nat, O, S


class Constraint:
    def __init__(self, lhs, rhs=None):
        if rhs is None:
            lhs, rhs = lhs
        self.eq = (lhs, rhs)
        self.lhs = lhs
        self.rhs = rhs

    def __getitem__(self, i):
        return self.eq[i]

    def __repr__(self):
        return str(self[0]) + " == " + str(self[1])


class UnificationException(Exception):
    pass


class OccursCheckException(UnificationException):
    def __init__(self, equation):
        self.equation = equation

    def __str__(self):
        return "Occurs Check failed: " + str(self.equation)


class ConflictException(UnificationException):
    def __init__(self, equation):
        self.equation = equation

    def __str__(self):
        return "Conflicting equation: " + str(self.equation)


class TypeConflictException(UnificationException):
    """Parameter conflict should be of the form ((term1, type1),(term2, type2))"""
    def __init__(self, equation, conflict: tuple):
        self.equation = equation
        self.confl = conflict

    def __str__(self):
        return f"Term ({str(self.confl[0][0])} : {str(self.confl[0][1])}) cannot be unified with" \
                   f" ({str(self.confl[1][0])} : {str(self.confl[1][1])}) in equation: " + str(self.equation)


def substitute(constraints, var, subs):
    return [Constraint(l.substitute(var, subs), r.substitute(var, subs)) for l, r in constraints]


def unify(constraints, verbose=False):
    # This algorithm comes from
    # https://en.wikipedia.org/wiki/Unification_(computer_science)#A_unification_algorithm
    # TODO: utilize the union-find algorithm to sort the result.
    solutions = []
    while constraints:
        c = constraints.pop()
        if verbose:
            print("Current Equations State:\n" + "\n".join([str(e) for e in constraints])
                  + "\n+++++++++++++++++++\n" + str(c) + "\n")
        if c[0] == c[1]:  # DELETE
            pass
        elif isinstance(c[0], Function) and isinstance(c[1], Function):
            if c[0].constructor == c[1].constructor:  # DECOMPOSE
                constraints.extend(map(Constraint, zip(c[0].args, c[1].args)))
            else:  # CONFLICT
                return ConflictException(c)
        elif isinstance(c[0], Function) and isinstance(c[1], Variable):  # SWAP
            constraints.append(Constraint(c[1], c[0]))
        elif isinstance(c[1], Term) and isinstance(c[0], Variable):
            if c[0] not in c[1].variables():  # ELIMINATE
                if c[0].type() != c[1].type():  # TYPE CONFLICT
                    raise TypeConflictException(c, ((c[0], c[0].type()), (c[1], c[1].type())))
                else:
                    constraints = substitute(constraints, c[0], c[1])
                    # constraints.insert(0, c)
                    solutions.append(c)
            else:  # OCCURS CHECK
                raise OccursCheckException(c)
        else:
            print("HERE!!!!!!!!!!!!!!!!!!1")
    return solutions


def constr(name, arity):
    return Constructor(name, Type0, (Type0,)*arity)


def vriabl(name):
    return Variable(name, Type0)


if __name__ == "__main__":
    f = constr("f", 1)
    c = constr("c", 0)
    g = constr("g", 2)
    x = vriabl("x")
    y = vriabl("y")
    z = vriabl("z")

    print("##### Test 1")
    expr = g(f(x), g(c(), y))
    eqs = [Constraint(expr, z), Constraint(f(y), f(g(x, c())))]
    sl = unify(eqs, True)
    print(sl)
    input("Paused...")

    print("##### Test 2")
    eqs = [Constraint(x, y), Constraint(y, f(x))]
    try:
        sl = unify(eqs, True)
    except OccursCheckException as e:
        print(e)
    input("Paused...")

    print("##### Test 3")
    A = Constructor("A", Type0, (Nat, Type0))
    n = Variable("n", Nat)
    eqs = [Constraint(A(n, x), y), Constraint(n, x)]
    print(isinstance(eqs[1][0], Variable))
    try:
        sl = unify(eqs, True)
    except TypeConflictException as e:
        print(e)
