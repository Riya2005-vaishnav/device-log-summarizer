
import math


def clean_sensor_readings(readings):
    """
    Clean and normalize sensor readings.

    Rules:
    1. Convert valid values to floats.
    2. Remove None, invalid values, and negative numbers.
    3. Remove NaN values.
    4. Cap values greater than 500.0 at 500.0.
    5. Return an empty list if no valid readings exist.
    """
    if readings is None:
        return []

    cleaned_readings = []

    for value in readings:
        if value is None:
            continue

        try:
            number = float(value)
        except (ValueError, TypeError, OverflowError):
            continue

        # Remove negative values and NaN
        if number < 0 or math.isnan(number):
            continue

        # Cap readings at 500.0
        number = min(number, 500.0)

        cleaned_readings.append(number)

    return cleaned_readings


# Test cases
assert clean_sensor_readings(
    [100, "250.5", None, -10, "invalid", 600, 0]
) == [100.0, 250.5, 500.0, 0.0]

assert clean_sensor_readings([]) == []

assert clean_sensor_readings(
    [None, "abc", -5, -10, ""]
) == []

assert clean_sensor_readings(None) == []

print("All tests passed.")
