"""Implements typed lambda calculus."""
from .basic import *


class To(Constructor):
    # (->) is of type Ui -> Uj -> U(max i,j)
    def __init__(self, l_level, r_level):
        super().__init__("To", Type(max(l_level, r_level)), (Type(l_level), Type(r_level)))

    def __call__(self, *variables):
        if len(variables) != 2 or any([variables[i].type() != t for i, t in enumerate(self.argtype)]):
            raise ValueError("Ill typing for constructor "+repr(self) + ", variables:" + str(variables))
        return FunctionType(self, variables)


class FunctionType(Function):
    def __repr__(self):
        return f"({repr(self.args[0])} -> {repr(self.args[1])})"


class BoundVariable(Variable):
    def __init__(self, name, t, bound):
        super().__init__(f"BV{str(id(bound))}_{name}", t)
        self.bound = bound

    def __eq__(self, other):
        return isinstance(other, BoundVariable) and self.name == other.name

    def variables(self):
        return set()


class Lambda(Term):
    def __init__(self, var: Variable, expr: Term):
        self.bv = BoundVariable("lambda_variable", var.type(), self)
        self.body = expr.substitute(var, self.bv)

    def __eq__(self, other):  # alpha conversion and no eta conversion
        return isinstance(other, Lambda) and self.body == other.body.substitute(other.bv, self.bv)

    def __repr__(self):
        return f"lambda {repr(self.bv)}.({repr(self.body)})"

    def substitute(self, var, sub):
        if var == self.bv:
            raise Warning("Are you trying to externally manipulate a bound variable?")
        return Lambda(self.bv, self.body.substitute(var, sub))

    def variables(self):
        return self.body.variables()

    def __hash__(self):
        return hash(self.bv) ^ hash(self.body)

    def type(self):
        return None  # TODO

    def reduce(self):  # beta reduction todo eta reduction
        return Lambda(self.bv, self.body.reduce())


class Application(Term):
    def __init__(self, head: Term, body: Term):
        pass

