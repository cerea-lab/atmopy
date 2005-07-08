from pylab import *


def segplot(x, y, fmt, maxdelta, **kwargs):
    """
    Plots x versus y, breaking the plot at any point where x[i] -
    x[i-1] > maxdelta. kwargs are passed on to plot
    """
    x = asarray(x)
    y = asarray(y)
    d = diff(x)
    lines = []
    ind = nonzero(greater(d, maxdelta))
    ind = ind+1
    if not len(ind):
        lines.extend( plot(x,y,fmt,**kwargs) ) 
    else:
        allind = [0]
        allind.extend(ind)
        allind.append(len(x))
        for i1,i2 in zip(allind[:-1], allind[1:]):
            lines.extend( plot(x[i1:i2], y[i1:i2], fmt, **kwargs) )
    return lines
        
def segplot_date(x, y, fmt, maxdelta, **kwargs):
    """
    Plots x versus y with dates, breaking the plot at any point where
    x[i] - x[i-1] > maxdelta. kwargs are passed on to plot
    """
    x = asarray(x)
    y = asarray(y)
    d = diff(x)
    lines = []
    ind = nonzero(greater(d, maxdelta))
    ind = ind+1
    if not len(ind):
        lines.extend(plot_date(x,y,fmt,**kwargs) ) 
    else:
        allind = [0]
        allind.extend(ind)
        allind.append(len(x))
        for i1,i2 in zip(allind[:-1], allind[1:]):
            lines.extend(plot_date(x[i1:i2], y[i1:i2], fmt, **kwargs) )
    return lines

def set_style1(lines):
    """
    Sets parameters for specified lines, style #1.
    """
    set(lines, \
        antialiased = True, \
        color = 'r', \
        linestyle = '-', \
        linewidth = 1.5)
    grid(True)
    yearsFmt = DateFormatter('%d/%m/%y')
    axes().xaxis.set_major_locator(WeekdayLocator())
    axes().xaxis.set_minor_locator(DayLocator())
    axes().xaxis.set_major_formatter(yearsFmt)
    labels = axes().get_xticklabels()
    set(labels, rotation=60)
    draw()

def set_style2(lines):
    """
    Sets parameters for specified lines, style #2.
    """
    set(lines, \
        antialiased = True, \
        color = 'b', \
        linestyle = '--', \
        linewidth = 1.0)
    grid(True)
    yearsFmt = DateFormatter('%d/%m/%y')
    axes().xaxis.set_major_locator(WeekdayLocator())
    axes().xaxis.set_minor_locator(DayLocator())
    axes().xaxis.set_major_formatter(yearsFmt)
    labels = axes().get_xticklabels()
    set(labels, rotation=60)
    draw()

def set_style_fromconfig(config, section, lines):
    """
    Searches for style variables in specified section of configstream,
    and applies the style to the given lines.
    Style must have following entries :
    antialiased (True/False)
    color (r,y,...)
    linestyle (-, --, ...)
    linewidth (float)
    grid (True/False)
    date_format (date format, ie %d/%m/%y)
    labels_rotation (integer)
    For more details, see matplotlib reference page.
    """
    antialiased_arg = config.GetElement("antialiased", section)
    color_arg = config.GetElement("color", section)
    linestyle_arg = config.GetElement("linestyle", section)
    linewidth_arg = config.GetElement("linewidth", section)
    grid_arg = config.GetElement("grid", section)
    date_format = config.GetElement("date_format", section)
    labels_rotation = config.GetElement("labels_rotation", section)        
    set(lines, \
        antialiased = antialiased_arg, \
        color = color_arg, \
        linestyle = linestyle_arg, \
        linewidth = linewidth_arg)
    grid(grid_arg)
    yearsFmt = DateFormatter(date_format)
    axes().xaxis.set_major_locator(WeekdayLocator())
    axes().xaxis.set_minor_locator(DayLocator())
    axes().xaxis.set_major_formatter(yearsFmt)
    labels = axes().get_xticklabels()
    set(labels, rotation=labels_rotation)
    draw()

    
