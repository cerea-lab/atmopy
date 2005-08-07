# Copyright (C) 2005 CEREA
#     Authors: Vivien Mallet
#
# CEREA (http://www.enpc.fr/cerea/) is a joint laboratory of
# ENPC (http://www.enpc.fr/) and EDF R&D (http://www.edf.fr/).
#
# This file is part of AtmoPy package.
# AtmoPy is a tool for data processing and visualization in atmospheric
# sciences.
#
# AtmoPy is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# AtmoPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License (file ``license'') for more details.
#
# For more information, please see the AtmoPy home page:
#     http://www.enpc.fr/cerea/atmopy/


import sys


def is_num(str):
    """
    Tests whether a string is a number.

    @type str: string
    @param str: String to be tested.

    @rtype: Boolean
    @return: True if 'str' is a number, False otherwise.
    """
    is_num = True
    try:
        num = float(str)
    except ValueError:
        is_num = False
    return is_num


def is_int(str):
    """
    Tests whether a string is an integer.

    @type str: string
    @param str: String to be tested.

    @rtype: Boolean
    @return: True if 'str' is a integer, False otherwise.
    """
    is_num = True
    try:
        num = int(str)
    except ValueError:
        is_num = False
    return is_num


def to_num(str):
    """
    Converts a string to a number.

    @type str: string
    @param str: String to be converted.

    @rtype: int (preferred) or float
    @return: The number represented by 'str'.
    """
    if is_int(str):
        return int(str)
    elif is_num(str):
        return float(str)
    else:
        raise Exception, "\"" + str + "\" is not a number."


def remove_file(files):
    """
    Removes one or more files and/or directories (without confirmation).

    @type files: string or list of strings
    @param files: files and directories to be removed.
    """
    if isinstance(files, str):
        files = [files]
    if not isinstance(files, list):
        raise ValueError
    for file in files:
        import os
        if os.path.isdir(file):
            import shutil
            shutil.rmtree(file)
        elif os.path.isfile(file):
            os.remove(file)


def apply_module_functions(module, args, functions = ("all", )):
    """
    Applies functions (with the right number of arguments) from a given module
    to the arguments of 'args'.

    @type module: module
    @param module: The module in which the functions are found.
    @type args: list
    @param args: The arguments to call the functions with.
    @type function: list of string
    @param function: The list of functions to be applied. If 'functions'
    contains 'all', then all functions are applied (only once).

    @rtype: (list of string, list)
    @return: The list of applied functions and the list of results.
    """
    Nargs = len(args)
    import inspect, types
    if "all" in functions:
        functions = [x for x in dir(module)
                     if inspect.isfunction(getattr(module, x))]
    out_functions, results = [], []
    for f in functions:
        if len(inspect.getargspec(getattr(module, f))[0]) == Nargs:
            out_functions.append(f)
            results.append(getattr(module, f)(*args))
    return out_functions, results


def get_module_functions(module, Nargs, functions = ("all", )):
    """
    Lists the functions, with 'Nargs' arguments, from a given module.

    @type module: module
    @param module: The module in which the functions are found.
    @type args: integer
    @param args: The number of arguments.
    @type function: list of string
    @param function: The list of functions to be possibly listed. If
    'functions' contains 'all', then all functions are listed (only once).

    @rtype: (list of string, list)
    @return: The list of functions that could be called with 'Nargs'
    arguments.
    """
    import inspect, types
    if "all" in functions:
        functions = [x for x in dir(module)
                     if inspect.isfunction(getattr(module, x))]
    out_functions = []
    for f in functions:
        if len(inspect.getargspec(getattr(module, f))[0]) == Nargs:
            out_functions.append(f)
    return out_functions


class PrintInPlace:
    """
    PrintInPlace enables to write and overwrite data on screen.
    """
    def __init__(self, length = 0):
        """
        @type length: integer
        @param length: Number of characters to be overwritten next time
        something is printed on screen.
        """
        self.length = length
    def __call__(self, elt):
        """
        Prints a string on screen.

        @type elt: string
        @param elt: String to be printed on screen.
        """
        sys.stdout.write(chr(8) * self.length + ' ' * self.length \
                         + chr(8) * self.length + str(elt))
        sys.stdout.flush()
        self.length = len(str(elt))
    def Print(self, elt):
        """
        Prints a string on screen.

        @type elt: string
        @param elt: String to be printed on screen.
        """
        self.__call__(elt)
    def Reinit(self):
        """
        Reinits the instance: no character is removed next time something is
        printed on screen.
        """
        self.length = 0
    def Clear(self, elt = ''):
        """
        Reinits the instance: no character is removed next time something is
        printed on screen, and the characters that were supposed to be
        overwritten are cleared. A last string may be printed.

        @type elt: string
        @param elt: The last string to be printed.
        """
        sys.stdout.write(chr(8) * self.length + ' ' * self.length \
                         + chr(8) * self.length + str(elt))
        sys.stdout.flush()
        self.length = 0


def print_stdout_file(elt, file, end_line = True):
    """
    Prints an element on standard output and in a file (if ready).

    @type elt: convertible to string
    @param elt: The element to be printed.
    @type file: file descriptor or None
    @param file: The file into which the element is to be printed. If nothing
    is to be printed in a file, 'file' should be None.
    @type end_line: Boolean
    @param end_line: True if a line break should be appended after 'elt',
    False otherwise.
    """
    output = str(elt)
    if end_line:
        output += '\n'
    sys.stdout.write(output)
    sys.stdout.flush()
    if file != None:
        file.write(output)
        file.flush()
