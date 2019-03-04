from HoTTcore.basic import *

"""Implements Intuitionistic Type Theory."""


class WeakInductive(Term):
    """Implements the inductive type similar to that of Coq's.
It is called `WeakInductive` because it is weaker than the W-type.
This type is defined in order to uniformly define other types."""
    def __init__(self, name: str, cons: map):
        """cons should be a map from constructor names to their argument types.
Use None in place of the type itself."""
        self.name = name
        self.constructors = {c: Constructor(c, self, tuple([t if t is not None else self for t in cons[c]]))
                             for c in cons}
        self.recursor = None  # TODO
        self.induction = None  # TODO
        self.eliminator = None
        self.computation = None
        self.uniqueness = None  # optional

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

Nat = WeakInductive("Nat", {"O": (), "S": (None,)})
O = Nat.constructors["O"]()
S = Nat.constructors["S"]

if __name__ == "__main__":
    x = Variable("x", Bool)
    nat_three = S(S(S(O)))
    print(nat_three)
