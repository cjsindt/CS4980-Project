Policy.py

This file requires pandas and matplotlib.

Using the data in the /data directory, this file contains functions that generate a plot of policies at certain thresholds.

For example, calling "containment_closing_1('New York')" will generate a time-series stacked-bar plot of all policies relating to containment and closure within New York that meet a threshold of at least 1 (According to the OxCGRT rating scale for that policy).
This plot is both shown at runtime and saved to the ./plots/ directory as "<state name>_containment_closure_1.png".
Naming conventions follow the same pattern for different thresholds and categories.