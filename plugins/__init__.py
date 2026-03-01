"""
plugins/__init__.py
Plugins package — input readers and output writers.
"""

from plugins.inputs import JSONReader, CSVReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter

__all__ = [
    "JSONReader",
    "CSVReader",
    "ConsoleWriter",
    "GraphicsChartWriter",
]