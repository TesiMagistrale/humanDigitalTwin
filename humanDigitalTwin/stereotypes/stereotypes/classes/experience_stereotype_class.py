from typing import Callable
"""
This module provides functions for calculating weight based on experience class.
"""

def _compute_drive_experience_and_frequence_value(licence_year: int, yearly_km: int):
    """
    Calculate a weight factor based on driving experience and mileage.

    Args:
        licence_year (int): Number of years of driving experience.
        yearly_km (int): Total kilometers driven in the past year.

    Returns:
        float: The calculated weight factor.
    """     
    experience = 2 if licence_year <= 2 else 1
    w = 0
    if yearly_km in range(0, 2000):
        w = 0.1
    elif yearly_km in range(2000, 5000):
        w = 0.05
    else:
        w = 0
    return w*experience

_compute_drive_experience_and_frequence_weight: Callable[[int, int], float] = _compute_drive_experience_and_frequence_value

def drive_experience_and_frequence_weight(licence_year: int, yearly_km: int) -> float:
    """
    Calculate a weight factor based on driving experience and mileage.

    Args:
        licence_year (int): Number of years of driving experience.
        yearly_km (int): Total kilometers driven in the past year.

    Returns:
        float: The calculated weight factor.
    """     
    return _compute_drive_experience_and_frequence_weight(licence_year, yearly_km)

def update_compute_drive_experience_and_frequence_weight(function: Callable[[int, int], float]):
    """ Update the value of the function variable _compute_drive_experience_and_frequence_weight
    Args:
    function (Callable[[int, int], float]): a function that compute the weight of experience and frequence for the driving task 
    """
    global _compute_drive_experience_and_frequence_weight
    _compute_drive_experience_and_frequence_weight = function
