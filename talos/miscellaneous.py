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
