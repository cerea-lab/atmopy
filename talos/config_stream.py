import commands
import datetime
    
class ConfigStream:
    """Manages a configuration file. The ConfigStream class provides
    an interface to the Talos config file system, through calls to
    the extract_configuration program."""
    def __init__(self, file):
        self.filename = file
    def GetOutput(self, command):
        """ Calls external program extract_configuration (which must
        be in the PATH), and returns output of execution on success.
        Raises exception on failure.
        """
        (s, o) = commands.getstatusoutput("extract_configuration " \
                                          + self.filename + " " + \
                                          command)
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
    def GetElement(self, element, section = ""):
        """Returns specified element value in given section (string)."""
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
                                 
                                                        

