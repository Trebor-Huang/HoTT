from HoTTcore.infrastructure import *
from HoTTcore.unification import *

"""Implements Intuitionistic Type Theory."""


class Type(Expression):
    """Base class for the expression of types."""
    pass


class Polymorph(Type):
    """Class for type variables for polymorphic types."""
    pass


class TypeConstructor(Constructor):
    """Class for type constructors."""
    pass


class Inductive(Type):
    """Class for types created from TypeConstructor."""
    pass
