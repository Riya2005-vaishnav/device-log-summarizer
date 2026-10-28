# Device Log Summarizer

CLI tool that reads device telemetry from a CSV, aggregates it per device, filters out
devices with an average temperature above 80.0, and exports the result as JSON.

## Requirements
- Python 3.9+
- `matplotlib` (only for the chart): `pip install matplotlib`

## Run
```
python sanitize.py
python summarizer.py --input device_telemetry.csv --output output.json
python plot_chart.py
```

## Behavior
- Rows with a missing device_id or a non-numeric/missing temperature are skipped and counted.
- Missing file, missing columns, empty file or unwritable output exit with a clear error message.
- Devices with average temperature > 80.0 are excluded (change with `--max-avg-temp`).
- `plot_chart.py` reads `output.json` and saves `chart.png`.

## Files
- `sanitize.py` - Section 1: sensor value cleaning + tests
- `summarizer.py` - Section 2: CSV aggregation CLI
- `plot_chart.py` - Section 3: bar chart of average temperature per device
- `device_telemetry.csv` - sample input data created for testing (the original file was not received)
- `output.json`, `chart.png` - sample outputs
- `PROMPT_LOG.md` - how AI tools were used