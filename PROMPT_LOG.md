# Prompt Log

## AI tool used
ChatGPT   

## 1. Initial prompt
> Write a Python script that loads output.json (a list of objects with device_id and avg_temperature) and generates a bar chart of average temperature per device using matplotlib. Save it as chart.png.

## 2. Bug / formatting mistake in the AI's first attempt
The y-axis label was just "Average Temperature" with no unit, so the chart did not show whether the values were in °C or °F. The bars also had no value labels, so exact numbers could not be read, and the script had no error handling for a missing output.json.

## 3. Follow-up prompt used to fix it
> The chart works, but the y-axis label has no unit and the bars don't show their values. Please update the script to: 1) label the y-axis "Average Temperature (°C)", 2) show the exact value above each bar, and 3) print a clear error message instead of crashing if output.json is not found.

## Result
The second version labels the y-axis "Average Temperature (°C)", shows each bar's exact value, and prints a clear error if output.json is missing. I ran it and checked chart.png to confirm the fixes.

## Notes
- Section 1 (`sanitize.py`) was written by me. I used an AI assistant only to review it afterwards, which led to adding NaN and None-input handling and switching the tests to asserts.
- Sections 2 and 3 used AI assistance. I tested the summarizer with sample data, including rows with bad values, and ran the chart script myself.