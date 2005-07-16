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


def apply_module_functions(module, args):
    """
    Applies all functions (with the right number of arguments) from a given
    module to the arguments of 'args'.

    @type module: module
    @param module: The module in which the functions are found.
    @type args: list
    @param args: The arguments to call the functions with.

    @rtype: (list of string, list)
    @return: The list of the applied functions and the list of the results.
    """
    Nargs = len(args)
    functions = []
    results = []
    import inspect, types
    for f in [x for x in dir(module) \
              if inspect.isfunction(getattr(module, x))]:
        if len(inspect.getargspec(getattr(module, f))[0]) == Nargs:
            functions.append(f)
            results.append(getattr(module, f)(*args))
    return functions, results


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
    def Clear(self):
        """
        Reinits the instance: no character is removed next time something is
        printed on screen, and the characters that were supposed to be
        overwritten are cleared.
        """
        sys.stdout.write(chr(8) * self.length + ' ' * self.length \
                         + chr(8) * self.length)
        sys.stdout.flush()
        self.length = 0


def print_stdout_file(elt, file, end_line = True):
    """
    Prints an element on standard output and in a file.

    @type elt: convertible to string
    @param elt: The element to be printed.
    @type file: file descriptor
    @param file: The file into which the element is to be printed.
    @type end_line: Boolean
    @param end_line: True if a line break should be appended after 'elt',
    False otherwise.
    """
    output = str(elt)
    if end_line:
        output += '\n'
    sys.stdout.write(output)
    sys.stdout.flush()
    file.write(output)
    file.flush()
