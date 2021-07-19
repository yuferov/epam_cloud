#! /usr/bin/python

import math

variables = [ 42, 45.0, True, False, [16, 9, 43, 65, 97, 0]]

def print_type(variables):
    for variable in variables:
        print(type(variable))

def do_action(variables):
    print_type(variables)
    for variable in variables:
        if isinstance(variable, bool):
            print(not variable)
        elif isinstance(variable, float):
            print(variable+math.pi)
        elif isinstance(variable, list):
            print(list(reversed(variable)))
        elif isinstance(variable, int):
            print(variable**2)
        else:
            ("idk")

do_action(variables)
