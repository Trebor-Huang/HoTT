"""Implements lambda calculus."""
from .basic import *


class To(Constructor):
    def __init__(self, intype: tuple, outtype):
        pass

    def __eq__(self, other):
        pass

    def __repr__(self):
        pass

    def __call__(self, *variables):
        pass

    def __hash__(self):
        pass

# TODO a new type for bounded variable


class Lambda:
    pass
