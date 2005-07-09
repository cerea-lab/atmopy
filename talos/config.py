# Copyright (C) 2005 CEREA
#     Author: Vivien Mallet
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


import config_stream


class Config:
    """
    Instances of Config store a complete configuration extracted from a
    configuration file.
    """

    def __init__(self, filename, additional_content = [], new_content = []):
        """
        Config constructor. It reads a set of attributes in a configuration
        file.

        @type filename: string
        @param filename: The name of the configuration file.
        @type additional_content: list of tuples of strings
        @type additional_content: Description of attributes (in addition to
        the default attributes) read in the configuration file. There are
        three or four elements in each tuple:
        0. the field name or section name (in case a whole section is put in
        the attribute), to be read in the configuration file;
        1. the section name (in which the field lies), discarded in case a
        whole section is read;
        2. the name of the attribute, optional (default: the field name);
        3. the type of the attribute: 'Int', 'IntList', 'IntSection', 'Float',
        'FloatList', 'FloatSection', 'String', 'StringList' or
        'StringSection', where 'Section' means that a whole section is read
        and returned in a list made of the section lines.
        @type new_content: list of tuples of strings
        @type new_content: Description of all attributes. It overwrites the
        default attributes.
        """
        self.filename = filename
        self.stream = config_stream.ConfigStream(self.filename)
        self.content = [("t_min", "[input]", "Float"), \
                        ("x_min", "[input]", "Float"), \
                        ("y_min", "[input]", "Float"), \
                        ("Delta_t", "[input]", "Float"), \
                        ("Delta_x", "[input]", "Float"), \
                        ("Delta_y", "[input]", "Float"), \
                        ("Nt", "[input]", "Int"), ("Nx", "[input]", "Int"), \
                        ("Ny", "[input]", "Int"), ("Nz", "[input]", "Int"), \
                        ("file", "[input]", "input_file", "String"), \
                        ("species", "[input]", "String"), \
                        ("obs_dir", "[input]", "String"), \
                        ("station_file", "[input]", "String"), \
                        ("type", "[output]", "String"), \
                        ("terminal", "[output]", "String"), \
                        ("t_range", "[output]", "IntList"), \
                        ("x_range", "[output]", "IntList"), \
                        ("y_range", "[output]", "IntList"), \
                        ("station", "[output]", "String"), \
                        ("file", "[output]", "output_file", "String"), \
                        ("[species_list]", "", "species_list", "StringSection"), \
                        ("[dir_list]", "", "dir_list", "StringSection"), \
                        ("[file_list]", "", "file_list", "StringSection")]
        self.content.append(additional_content)
        if len(new_content) != 0:
            self.content = new_content[:]
        for x in self.content:
            self.SetAttribute(x)

    def SetAttribute(self, x):
        """
        Sets an attribute based on its value in the configuration file. If the
        corresponding field does not appear in the configuration files, the
        attribute is not created.

        @type x: list of lists of strings
        @param x: Each element of x contains three or four elements:
        0. the field name or section name (in case a whole section is put in
        the attribute), to be read in the configuration file;
        1. the section name (in which the field lies), discarded in case a
        whole section is read;
        2. the name of the attribute, optional (default: the field name);
        3. the type of the attribute: 'Int', 'IntList', 'IntSection', 'Float',
        'FloatList', 'FloatSection', 'String', 'StringList' or
        'StringSection', where 'Section' means that a whole section is read
        and returned in a list made of the section lines.
        """
        try:
            val = self.stream.GetElement(x[0], section = x[1], type = x[-1])
            if len(x) == 4:
                setattr(self, x[2], val)
            else:
                setattr(self, x[0], val)
        except:
            pass
