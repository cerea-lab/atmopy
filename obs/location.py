class Station:
    "Stores information about an observation station"
    name = ""
    latitude = 0.0
    longitude = 0.0
    country = ""
    aasqa = ""
    type1 = ""
    type2 = ""

    def __init__(self, str=""):
        self.FromString(str)
        
    def FromString(self, str):
        """ Sets station's attributes from string."""
        if str != "":
            values = str.strip().split()
            try:
                self.longitude = float(values[0])
            except ValueError:
                self.longitude = 0.0                
            try:
                self.latitude = float(values[1])
            except ValueError:
                self.latitude = 0.0                
            self.country = values[4]
            self.type1 = values[5]
            self.type2 = values[6]
            self.name = values[7]
            self.asqa = values[8]
        
    def FromFile(self, filename, station_name):
        """ Loads station's attributes from text file."""
        try:
            f = open(filename, "r", 0)
            line = f.readline()
            while station_name != self.name and line != "":
                line = f.readline()
                self.FromString(line)
            f.close()
        except IOError:
            pass
                
    def __str__(self):
        return self.name + " (" + str(self.latitude) + ", " \
               + str(self.longitude) + ") " \
               + self.country + " " \
               + self.type1 + " " \
               + self.type2 + " " \
               + self.asqa

    def IsInsideBox(lat_min, lat_max, lon_min, lon_max):
        """ Check wether the station is inside a given area.
        Returns Boolean.
        """
        return self.latitude >= lat_min \
               and self.latitude <= lat_max \
               and self.longitude >= lon_min \
               and self.longitude <= lon_max

    def IsInsideGridBox(origins, deltas, lengths):
        """ Check wether the station is located inside a given
        area defined by (lat, lon) origins, deltas on and lengths of
        cells.
        Returns Boolean.
        """
        return IsInsideBox(origins[0], \
                           origins[0]
                           + deltas[0] * float(lengths[0]), \
                           origins[1], \
                           origins[1], \
                           + deltas[1] * float(lengths[1]))

def filter_urban(station):
    """ Returns true if the station is of urban type, false otherwise.
    Returns Boolean."""
    return station.type1 == "URB"

def filter_rural(station):
    """ Returns true if the station is of rural type, false otherwise.
    Returns Boolean."""
    return station.type1 == "RUR"

def filter_notnull_latlon(station):
    """ Returns True if the station has not-null latitude and longitude,
    False otherwise.
    Returns Boolean."""
    return station.latitude != 0.0 and station.longitude != 0.0

def get_simulated_at_locations(data, point_list, origins, deltas):
    """ Gets a a list of time sequences of data at specified
    locations using bilinear interpolation.
    Returns list of 1D arrays.
    """
    ret = []
    for i in point_list:
        ret.append(get_simulated_at_location(data, i, origins, deltas))
    return ret
                  
def get_simulated_at_stations(data, stations, origins, deltas):
    """ Gets a a list of time sequences of data at specified
    stations locations using bilinear interpolation.
    Returns list of 1D arrays.
    """
    ret = []
    for i in stations:
        ret.append(get_simulated_at_station( \
            data, i, origins, deltas))
    return ret

def get_simulated_at_station(data, station, origins, deltas):
    """ Gets a time sequence of data at specified station
    using bilinear interpolation.
    Returns 1D array."""
    # data: numarray, T Y X
    # point: (latitude, longitude)
    # origins: (t_min, y_min, x_min)
    # deltas: (delta_t, delta_y, delta_x)
    return get_simulated_at_location( \
        data, (station.latitude, station.longitude), origins, deltas)

def get_simulated_at_location(data, point, origin, delta):
    """ Gets a time sequence of data at specified location
    using bilinear interpolation.
    Returns 1D array."""
    # data: numarray, T Y X
    # point: (latitude, longitude)
    # origin: (t_min, y_min, x_min)
    # delta: (delta_t, delta_y, delta_x)
    
    # Gets index of bottom right data point of specified point
    index_y = int((point[0] - origin[1]) / delta[1])
    index_x = int((point[1] - origin[2]) / delta[2])

    # Interpolation impossible.
    if index_x >= data.getshape()[2] or index_y >= data.getshape()[1] \
           or index_x < 0 or index_y < 0:
        return numarray.array([])

    # Interpolation coefficients.
    coeff_y = (point[0] - origin[1] - delta[1] * index_y) / delta[1]
    coeff_x = (point[1] - origin[2] - delta[2] * index_x) / delta[2]
    
    return (1.0 - coeff_y) * (1.0 - coeff_x) * data[:, index_y, index_x] \
           + coeff_y * coeff_x * data[:, index_y + 1, index_x + 1] \
           + coeff_y * (1.0 - coeff_x) * data[:, index_y + 1, index_x]  \
           + (1.0 - coeff_y) * coeff_x * data[:, index_y, index_x + 1]


def get_simulated_at_locations_closest(data, point_list, \
                                       origins, deltas):
    """ Gets a a list of time sequences of data at specified
    locations using closest point.
    Returns list of 1D arrays.
    """
    ret = numarray.array([])
    for i in point_list:
        ret.append(get_simulated_at_location_closest(data, i, \
                                                     origins, deltas))
    return ret

def get_simulated_at_location_closest(data, point, origins, deltas):
    """ Gets a time sequence of data at specified location.
    Returns 1D array."""
    # data : numarray, T Y X
    # point : ( latitude, longitude )
    # origins : ( Xmin, Ymin, Tmin )
    # deltas : ( DeltaX, DeltaY, DeltaT )

    # Closest point :
    index_y = int(round((point[0] - origin[1]) / delta[1]))
    index_x = int(round((point[1] - origin[2]) / delta[2]))

    # point is on right border
    if index_x == data.getshape()[2]:
        index_x = index_x - 1
    # point is on top border
    if index_y == data.getshape()[1]:
        index_y = index_y - 1
    return data[:,index_y, index_x]

def get_station(station_list, station_name):
    """ Gets a Station object given its name and a list of stations.
    Returns Station."""
    for i in station_list:
        if i.name == station_name:
            ret = i
            break
    return ret

def filter_stations(filter_func, station_list):
    """ Filters a station list in place according to the given filter.
    To have a filter not acting in place, use the filter python
    builtin.
    Returns Station list.
    """
    for i in range(len(station_list) - 1, -1, -1):
        if not filter_func(station_list[i]):
            station_list.pop(i)
    return station_list


def map_stations(bool_func, station_list):
    """ Returns a boolean list containing the return values of the
    given function applied on every station of the list.
    This just calls the map builtin function.
    Returns boolean list.
    """
    return map(bool_func, station_list)

def filter_stations_observations(filter_func, station_list, observations_list):
    """ Filters a station list and corresponding observations list in
    place according to the given filter which takes a station and an
    observation array in argument.
    Returns Station list and observation list (Array)."""
    for i in range(len(station_list) - 1, -1, -1):
        if not filter_func(station_list[i], observations_list[i]):
            station_list.pop(i)
            observations_list.pop(i)
    return station_list, observations_list

def map_stations_observations(map_func, station_list, observations_list):
    """ Returns a list containing the return values of the
    given function applied on every station and observation of the
    lists.
    Returns list.
    """
    ret = numarray.array([])
    for i in range(len(station_list)):
        ret.append(map_func(station_list[i], observations_list[i]))
    return ret
