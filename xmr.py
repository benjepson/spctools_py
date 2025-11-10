from dataclasses import dataclass
from typing import List, Union
from datetime import datetime
import statistics

@dataclass
class XmRResult:
    # timestamp of when calculation was performed
    timestamp: str
    # user notes describing project, context, etc (required, could be empty string)
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