import config_stream

class Config:
    """
    Instances of Config store a complete configuration extracted from a
    configuration file.
    """
    def __init__(self, filename, additional_content = [], new_content = []):
        self.filename = filename
        self.stream = config_stream.ConfigStream(self.filename)
        self.content = [("t_min", "[input]", "Float"), \
                        ("x_min", "[input]", "Float"), \
                        ("y_min", "[input]", "Float"), \
                        ("delta_t", "[input]", "Float"), \
                        ("delta_x", "[input]", "Float"), \
                        ("delta_y", "[input]", "Float"), \
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
        @param x: each element of x contains three or for elements:
        0. the field name (to be found in the configuration file);
        1. the section in which the field lies;
        2. the name of the attribute, optional (default: the field name);
        3. the type of the attribute ('Int', 'IntList', 'IntSection', 'Float',
        'FloatList', 'FloatSection', 'String', 'StringList' or
        'StringSection').
        """
        try:
            val = self.stream.GetElement(x[0], section = x[1], type = x[-1])
            if len(x) == 4:
                setattr(self, x[2], val)
            else:
                setattr(self, x[0], val)
        except:
            pass
