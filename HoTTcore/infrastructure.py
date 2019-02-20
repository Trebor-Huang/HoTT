class Expression:
    def __eq__(self, other):
        pass

    def __str__(self):
        pass

    def substitute(self, var, sub):
        pass

    def variables(self):
        pass


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return type(other) == Variable and self.name == other.name

    def __str__(self):
        return self.name

    def substitute(self, var, sub):
        if self == var:
            return sub
        else:
            return self

    def variables(self):
        return [self]


class Constructor:
    def __init__(self, name, arity=0):
        self.name = name
        self.arity = arity

    def __eq__(self, other):
        return type(other) == Constructor and self.name == other.name and self.arity == other.arity

    def __str__(self):
        return self.name + "/" + str(self.arity)

    def __call__(self, *variables):
        if len(variables) == 1 and type(variables[0])==tuple:
            variables = variables[0]
        if len(variables) != self.arity:
            raise ValueError("Incorrect arity for "+str(self)+".")
        return Function(self, variables)


class Function(Expression):
    def __init__(self, cons, variables):
        self.constructor = cons
        self.variables = tuple(variables)


