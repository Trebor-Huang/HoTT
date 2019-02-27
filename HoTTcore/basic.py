class Term:
    def __eq__(self, other):
        pass

    def __repr__(self):
        pass

    def substitute(self, var, sub):
        pass

    def variables(self):
        pass

    def __hash__(self):
        return 0

    def type(self):
        pass


class Variable(Term):
    def __init__(self, name, t):
        self.name = name
        self._t = t

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __repr__(self):
        return self.name

    def substitute(self, var, sub):
        if self == var:
            return sub
        else:
            return self

    def variables(self):
        return {self}

    def __hash__(self):
        return hash(self.name)

    def type(self):
        if self._t is None:
            return None
        else:
            return self._t


class Constructor:  # TODO: should be a function type???
    def __init__(self, name, returntype, argtype: tuple = None):
        self.name = name
        if argtype is None:
            argtype = ()
        self.argtype = argtype
        self.arity = len(argtype)
        self.rettype = returntype

    def __eq__(self, other):
        return isinstance(other, Constructor) and self.name == other.name and self.argtype == other.argtype

    def __repr__(self):
        return self.name + "/" + str(self.arity)

    def __call__(self, *variables):
        if len(variables) == 1 and isinstance(variables[0], tuple):
            variables = variables[0]
        if len(variables) != self.arity or any([variables[i].type() != t for i, t in enumerate(self.argtype)]):
            raise ValueError("Ill typing for constructor "+repr(self) + ", variables:" + str(variables))
        return Function(self, variables)

    def __hash__(self):
        return hash(self.name) ^ hash(self.argtype)


class Function(Term):
    def __init__(self, cons, variables):
        self.constructor = cons
        self.args = tuple(variables)
        self._t = self.constructor.rettype

    def __eq__(self, other):
        return isinstance(other, Function) and self.constructor == other.constructor and self.args == other.args

    def __repr__(self):
        return f"{self.constructor.name}({', '.join([str(v) for v in self.args])})"

    def substitute(self, var, sub):
        return self.constructor(tuple([v.substitute(var, sub) for v in self.args]))

    def variables(self):
        return set.union(set(), *[v.variables() for v in self.args])  # Empty set() to avoid empty unions

    def __hash__(self):
        return hash(self.constructor) ^ hash(self.args)

    def type(self):
        return self._t


class Type(Term):   # Got to wrap the Type hierarchy up...
    def __init__(self, level: int = 0):
        assert isinstance(level, int) and level >= 0
        self.level = level

    def __eq__(self, other):
        return isinstance(other, Type) and self.level == other.level

    def __repr__(self):
        return "U_" + str(self.level)

    def substitute(self, var, sub):
        return self

    def variables(self):
        return {}

    def __hash__(self):
        return hash(self.level) ^ hash(Type)

    def type(self):
        return Type(self.level + 1)  # There!


# A system to prevent many copies of Type(n) to be made
Type0 = Type(0)
Type1 = Type(1)
Types = {0: Type0, 1: Type1}


def get_type(level: int):
    if level in Types:
        return Types[level]
    Types[level] = Type(level)
    return Types[level]


if __name__ == "__main__":
    f = Constructor("f", Type0, (Type0,))
    c = Constructor("c", Type0)
    g = Constructor("g", Type0, (Type0, Type0))
    x = Variable("x", Type0)
    y = Variable("y", Type0)

    expr = g(f(x), g(c(), y))

    print(expr)
    print(expr.variables())

    expr1 = expr.substitute(x, g(y, f(c())))

    print(expr1)
    print(expr1.variables())
