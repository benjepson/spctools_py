from dataclasses import dataclass
from typing import List, Union
from datetime import datetime
import statistics

# define the output of the xmr function
@dataclass
class XmRResult:
    # timestamp of when calculation was performed
    timestamp: str
    # user notes describing project, context, etc (required)
    notes: str
    # X axis values, the order of the Y observations (sequence number, datetime, timepoints)
    # Must be all numeric (int/float) or all strings (dates)
    x: List[Union[int, float, str]]
    # Y axis values/observations, numeric taken at X
    y: List[float]
    # mean of all Y values
    mean: float
    # sigma based on moving range of successive Y values
    sigma: float
    # Upper and lower control limits(±2.66 * MRbar (avg moving range))
    ucl: float
    lcl: float
    # upper range limit (3.268 * MRbar)
    url: float
    # moving range values (padded with None at start to match X/Y length)
    mr: List[Union[None, float]]
    # mean of moving range
    mr_bar: float
    # standard deviation of all Y values
    # NOT used in XmR charts, but available for capability/performance calculations later
    stdev: float
    # warnings of validation messages
    warnings: List[str]

# define function to calculate xmr
def calculate_xmr(x, y, notes):
    """
    Calculate XmR chart statistics for a single series.
    
    Parameters:
        x (list): Sequence identifiers (e.g., timepoints, dates, or index values). Must be all numeric or all strings(dates).
        y (list): Numeric measurements. Must be convertible to float.
        notes (str): Required user notes describing intent, context, equipment, etc
    
    Returns:
        XmRResult: Structured object containing calculations, metadata, and warnings.
    """

    # Initialize warnings list
    warnings = []

    # Validate notes
    if not isinstance(notes, str) or len(notes.strip()) == 0:
        raise ValueError("User notes must be a non-empty string.")

    # Convert x and y to lists
    try:
        x = list(x)
        y = list(y)
    except Exception:
        raise ValueError("Inputs x and y must be convertible to lists.")

    # Validate lengths
    if len(x) != len(y):
        raise ValueError("x and y must be the same length.")
    # even 3 is probably not enough data, but 2 makes no sense. The moving range is just the difference between the 2 points
    # I'm allowing 3 as minimum because have to draw a line somewhere, but really should be more than 3
    if len(y) < 3:
        raise ValueError("XmR calculation requires at least 3 data points.")
    if len(y) < 10:
        warnings.append("Fewer than 10 data points, results may be unstable.")

    # Validate y is numeric
    try:
        y = [float(val) for val in y]
    except Exception:
        raise ValueError("All y values must be numeric.")

    # Validate x type consistency
    x_types = set(type(val) for val in x)
    if len(x_types) > 1:
        raise ValueError("All x values must be of the same type (int, float, or str).")

    # Warn if x is not evenly spaced (basic check)
    # X values don't have to be exactly evenly spaced but I'm trying to catch strange things since I don't know what the end user might do
    # for example if a measure is hourly and you took it 55 minutes apart then the next was 70 minutes apart might not matter
    # But if one was 10 minutes apart and the next was 2 days, that's inconsistent
    # will add more helpful testing and messages here later 
    if isinstance(x[0], (int, float)):
        diffs = [x[i+1] - x[i] for i in range(len(x)-1)]
        if len(set(diffs)) > 1:
            warnings.append("x values are not evenly spaced—consider using consistent intervals.")

    # Capture timestamp
    timestamp = datetime.now().isoformat()

### Calculations ###

    # calculate mean of y
    mean = statistics.mean(y)

    # calculate moving ranges (mR), padded with None at start to match X/Y length
    mr = [None] + [abs(y[i+1] - y[i]) for i in range(len(y) -1)]

    #calculate mean of moving ranges (MRbar), excluding None (just the numbers)
    mr_bar = statistics.mean(mr[1:])

    # control limit calculations
    ucl = mean + 2.66 * mr_bar
    lcl = mean - 2.66 * mr_bar
    url = 3.268 * mr_bar

    # calculate sigma
    sigma = (2.66 / 3) * mr_bar
    # calculate standard deviation
    # NOT used in control charts, add to object for future capability calculations
    stdev = statistics.stdev(y)

    # return the results
    return XmRResult(
        timestamp=timestamp,
        notes=notes,
        x=x,
        y=y,
        mean=mean,
        sigma=sigma,
        ucl=ucl,
        lcl=lcl,
        url=url,
        mr=mr,
        mr_bar=mr_bar,
        stdev=stdev,
        warnings=warnings
    )
