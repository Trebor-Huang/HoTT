from HoTTcore.basic import *
from HoTTcore.unification import *

"""Implements Intuitionistic Type Theory."""


class WeakInductive:
    """Implements the inductive type similar to that of Coq's.
It is called `WeakInductive` because it is weaker than the W-type.
This type is defined in order to uniformly define other types.
However, this does not define the recursor, induction principle, etc."""
    def __init__(self, name: str, cons: map):
        """cons should be a map from constructor names to their argument types.
Use None in place of the type itself."""
        pass
