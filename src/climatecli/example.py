"""Do something."""

from importlib import resources

import numpy as np
import yaml

_fn = resources.files("python_template.data").joinpath("some_data.yml").read_text()


def print_something(radius):
    """Print circumference of circle.

    Args:
        radius (float): Radius of circle.
    """
    print(f"Circle with radius {radius} has circumference {2 * np.pi * radius}")


def print_some_data():
    """Use useful data."""
    data = yaml.safe_load(_fn)
    for k, v in data.items():
        print(f"{k}: {v}")
