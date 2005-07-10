# Copyright (C) 2005 CEREA
#     Authors: Vivien Mallet, Vincent Picavet
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


import commands
import datetime


class ConfigStream:
    """Manages a configuration file. The ConfigStream class provides
    an interface to the Talos config file system, through calls to
    the extract_configuration program."""

    def __init__(self, file):
        import os.path
        self.filename = file
        self.extract = os.path.dirname(os.path.abspath(__file__)) \
                       + "/extract_configuration "

    def GetOutput(self, command):
        """ Calls external program extract_configuration (which must
        be in the PATH), and returns output of execution on success.
        Raises exception on failure.
        """
        (s, o) = commands.getstatusoutput(self.extract + self.filename \
                                          + " " + command)
        if s == 0:
            return o
        else:
            raise Exception, "Unable to launch: \"extract_configuration " \
                      + self.filename + " " + command + "\""

    def ListSections(self):
        """Lists all sections of config file."""
        return self.GetOutput("")

    def ListAll(self):
        """Lists everything in config file."""
        return self.GetOutput("-ll")

    def ListSectionLines(self, section):
        """Lists everything in specified section of config file."""
        return self.GetOutput("-s " + section)

    def GetElement(self, element, section = "", type = "String"):
        """
        Returns the value of a given field.

        @type element: string
        @param element: The element (field) to be found in the configuration
        file.
        @type section: string
        @param section: The section in which the element should be found, if any.
        @type type: string
        @param type: The type of the element to be returned. It could be:
        'Int', 'IntList', 'IntSection', 'Bool', 'Float', 'FloatList', 'FloatSection',
        'String',  'StringList' or 'StringSection'.

        @rtype: given by 'type'
        @return: The value of the field in the configuration file.

        @warning: In case the output is a list, the section is not taken into
        account, which means that two lists against the same field name should
        not be introduced in the configuration file, even in two different
        sections.
        """
        if type == "String":
            return self.GetString(element, section)
        elif type == "StringList":
            return self.ListSectionLines(element).split('\n')[0].split()
        elif type == "StringSection":
            return self.ListSectionLines(element).split('\n')
        elif type == "Int":
            return self.GetInt(element, section)
        elif type == "IntList":
            return [int(x) for x in \
                    self.ListSectionLines(element).split('\n')[0].split()]
        elif type == "IntSection":
            return [int(x) for x in self.ListSectionLines(element).split('\n')]
        elif type == "Bool":
            return self.GetBool(element, section)
        elif type == "Float":
            return self.GetFloat(element, section)
        elif type == "FloatList":
            return [float(x) for x in \
                    self.ListSectionLines(element).split('\n')[0].split()]
        elif type == "FloatSection":
            return [float(x) for x in self.ListSectionLines(element).split('\n')]
        else:
            raise Exception, "Type \"" + type + "\" is unknown."

    def GetString(self, element, section = ""):
        """
        Returns the value (string) of a given field.

        @type element: string
        @param element: The element (field) to be found in the configuration file.
        @type section: string
        @param section: The section in which the element should be found, if any.

        @rtype: string
        @return The value of the field in the configuration file.
        """
        if section == "":
            return self.GetOutput(element)
        else:
            return self.GetOutput("-s " + section + " " + element)

    def GetFloat(self, element, section = ""):
        """Returns specified element value in given section, as float"""
        if section == "":
            return float(self.GetOutput(element))
        else:
            return float(self.GetOutput("-s " + section + " " \
                                        + element))

    def GetInt(self, element, section = ""):
        """Returns specified element value in given section, as integer"""        
        if section == "":
            return int(self.GetOutput(element))
        else:
            return int(self.GetOutput("-s " + section + " " \
                                      + element))

    def GetBool(self, element, section = ""):
        """
        Returns the value (Boolean) of a given field.

        @type element: string
        @param element: The element (field) to be found in the configuration file.
        @type section: string
        @param section: The section in which the element should be found, if any.

        @rtype: Boolean
        @return The value of the field in the configuration file.
        """
        if section == "":
            elt = self.GetOutput(element)
        else:
            elt = self.GetOutput("-s " + section + " " + element)
        elt = elt.lower()
        if elt == "true" or elt == "t" or elt == "y" or elt == "yes":
            return True
        elif elt == "false" or elt == "f" or elt == "n" or elt == "no":
            return False
        else:
            raise Exception, "Field \"" + element + "\" is not a Boolean " \
                  "in " + self.filename + "."

    def GetDate(self, element, section = ""):
        """Returns specified element value in given section, converted
        into a datetime.datetime object with year, month and day.
        The value must be in the YYYYMMDD form."""
        ret_str = ""
        if section == "":
            ret_str = self.GetOutput(element)
        else:
            ret_str = self.GetOutput("-s " + section + " " + element)
        return datetime.datetime(int(ret_str[0:4]), int(ret_str[4:6]),
                                 int(ret_str[6:8]))

    def GetDateTime(self, element, section = ""):
        """Returns specified element value in given section, converted
        into a datetime.datetime object with year, month, day, hour, minutes
        and seconds.
        The value must be in the YYYYMMDDHHMMSS form."""
        ret_str = ""
        if section == "":
            ret_str = self.GetOutput(element)
        else:
            ret_str = self.GetOutput("-s " + section + " " + element)
        return datetime.datetime(int(ret_str[0:4]), int(ret_str[4:6]), \
                                 int(ret_str[6:8]), int(ret_str[8:10]),\
                                 int(ret_str[10:12]), int(ret_str[12:14]))
