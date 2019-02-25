from HoTTcore.basic import *
from HoTTcore.unification import *

"""Implements Intuitionistic Type Theory."""


class WeakInductive(Term):
    """Implements the inductive type similar to that of Coq's.
It is called `WeakInductive` because it is weaker than the W-type.
This type is defined in order to uniformly define other types.
However, this does not define the recursor, induction principle, etc."""
    def __init__(self, name: str, cons: map):
        """cons should be a map from constructor names to their argument types.
Use None in place of the type itself."""
        self.name = name
        self.constructors = {c: Constructor(c, self, cons[c]) for c in cons}

    def __eq__(self, other):
        return self is other  # intrinsic equality

    def __repr__(self):
        return self.name

    def substitute(self, var, sub):
        return self

    def variables(self):
        return {}

    def __hash__(self):
        return hash(self.name) ^ hash(self.constructors)

    def type(self):
        return Type0


Zero = WeakInductive("Zero", {})

Unit = WeakInductive("Unit", {"1": ()})
I_Unit = Unit.constructors["1"]

Bool = WeakInductive("Bool", {"T": (), "F": ()})
T_Bool = Bool.constructors["T"]
F_Bool = Bool.constructors["F"]

if __name__ == "__main__":
    x = Variable("x", Bool)
