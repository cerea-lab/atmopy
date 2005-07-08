def remove_lowest(data1, data2, dates, mini):
    """ Removes values of data1, data2 and dates where data1 values
    are lower than the given minimum.
    Returns arrays for data1 and data2, list for dates."""
    condition = (data1 > mini)
    for i in range(len(condition)-1, -1, -1):
        if condition[i] == 0:
            dates.pop(i)
    return data1[numarray.where(condition)], \
           data2[numarray.where(condition)], \
           dates
           
def remove_highest(data1, data2, dates, maxi):
    """ Removes values of data1, data2 and dates where data1 values
    are higher than the given maximum.
    Returns arrays for data1 and data2, list for dates."""
    condition = (data1 < maxi)
    for i in range(len(condition)-1, -1, -1):
        if condition[i] == 0:
            dates.pop(i)
    return data1[numarray.where(condition)], \
           data2[numarray.where(condition)], \
           dates

