"""
This module provides functions for calculating weight based on age class.
"""

def drive_age_weight(age:int) -> float:
    """
    Calculate a weight factor based on person age in driving task.

    Args:
        age (int): Driver age.

    Returns:
        float: The calculated weight factor.
    """
    import numpy as np
    STD = 10
    MEDIAN = 49
    MAX_RANGE = 1
    MIN_RANGE = 0.95
    
    def compute_age_value(std, median, max, min, x)-> float:
        normal_gaussian = np.exp(-np.power(x - median, 2.) / (2 * np.power(std, 2.)))
        return (max - min) * normal_gaussian + max
    
    MEDIAN_VALUE = compute_age_value(STD, MEDIAN, MAX_RANGE, MIN_RANGE, MEDIAN)
    
    age_value = compute_age_value(STD, MEDIAN, MAX_RANGE, MIN_RANGE, age)
    
    return MEDIAN_VALUE - age_value
    
    
    
