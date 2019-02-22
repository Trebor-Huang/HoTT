from HoTTcore.infrastructure import *
from HoTTcore.unification import *

"""Implements Intuitionistic Type Theory."""


class Type(Expression):
    """Base class for the expression of types."""
    def __init__(self):
        super().__init__()


class Polymorph(Variable, Type):
    """Class for type variables for polymorphic types."""
    def __init__(self, name):
        super().__init__(name)

    def __eq__(self, other):
        return isinstance(other, Polymorph) and self.name == other.name


class TypeConstructor(Constructor):
    """Class for type constructors."""
    def __init__(self, name, arity=0, getrepr=None):
        super().__init__(name, arity)
        self.getrepr = getrepr

    def __eq__(self, other):
        return isinstance(other, TypeConstructor) and self.name == other.name and self.arity == other.arity

    def __call__(self, *variables):
        if len(variables) == 1 and isinstance(variables[0], tuple):
            variables = variables[0]
        if len(variables) != self.arity:
            raise ValueError("Incorrect arity for "+str(self)+".")
        return Inductive(self, variables, self.getrepr)


class Inductive(Function, Type):
    """Class for types created from TypeConstructor."""
    def __init__(self, cons, variables, getrepr=None):
        super().__init__(cons, variables)
        self.getrepr = getrepr

    def __eq__(self, other):
        return isinstance(other, Function) and self.constructor == other.constructor and self.args == other.args

    def __repr__(self):
        if self.getrepr is not None:
            return self.getrepr(self)
        else:
            super().__repr__()


if __name__ == "__main__":
    alpha = Polymorph("\\alpha")
    beta = Polymorph("\\beta")
    impl = TypeConstructor("implication", 2, lambda self: str(self.args[0]) + " \\to " + str(self.args[1]))

    expr = impl(alpha, beta)
    print(expr)


# TODO: Implement the types.
