import numarray
import datetime

def get_filesize(filename):
    """Gets a file's size.
    Returns integer"""
    fileSize = 0
    try:
        f = open(filename, "r", 0)
        try:
            f.seek(0,2)
            fileSize = f.tell()
        finally:
            f.close()
    except IOError:
        pass
    return fileSize

def get_timesteps(filename, recordLength):
    """Gets number of timsteps in a file given its
    record length (in Bytes).
    Returns integer."""
    ts = 0
    if (recordLength != 0):
        ts = get_filesize / recordLength
    return ts

def save_binary(arrayToSave, filename, \
                dataType=numarray.numerictypes.Float32):
    """Saves a numarray in a binary file using specified type."""
    numarray.array(arrayToSave,
                   type=dataType).tofile(filename)

def load_binary(filename, shape, \
                dataType=numarray.numerictypes.Float32):
    """Loads a binary file into an array using specified shape.
    Returns numarray."""
    return numarray.fromfile(filename, dataType, shape)

def load_XYTbinary(filename, shape, \
                   dataType=numarray.numerictypes.Float32):
    """Loads a binary file into an array using specified 3D shape for
    X, Y and T dimensions (a time sequence of planes).
    If the given binary file is a 4D file (XYZT), the plane Z = 1 is
    extracted.
    """
    res = []
    zsize = get_filesize(filename) \
            / ( dataType.bytes * shape[0] * shape[1] * shape[2] )
    if zsize != 1:
        res = load_binary(filename, shape, dataType)
    else:
        newshape = list(shape)
        newshape.insert(1, zsize)
        # Use temp array to be sure that memory is freed
        temp = load_binary(filename, newshape, dataType)
        res = temp[:,1,:,:]
        del temp
    return res
