# every important class from every file is included here

"""
structuralcode.py

it shows the shape of every class and protocol in the system.
Actual implementation lives in core/engine.py and plugins/
"""

from typing import Protocol, List, Dict, Any, runtime_checkable


#  CORE , contracts (protocols / interfaces)
#  Core is  AUTHORITY ,owns all contracts

@runtime_checkable
class DataSink(Protocol):
    """Outbound abstraction — any output writer must implement this"""
    def write(self, data: List[Dict[str, Any]], title: str = "") -> None: ...


@runtime_checkable
class PipelineService(Protocol):
    """Inbound abstraction — input readers call this to send data to core"""
    def execute(self, raw_data: List[Dict[str, Any]]) -> None: ...


@runtime_checkable
class DataReader(Protocol):
    """Input abstraction — any reader must implement this"""
    def read(self) -> List[Dict[str, Any]]: ...


# ----------------------------
#  CORE ,engine (business logic)
#  Depends only on DataSink protocol -- never on concrete classes

class TransformationEngine:
    """Core engine — implements PipelineService, uses DataSink"""

    def __init__(self, sink: DataSink, config: dict) -> None:
        self.sink   = sink      # injected at runtime (DIP)
        self.config = config
        self.data   = None

    # ── filters ────────────────────────────────────────────────
    def filter_by_region(self, data, region: str): ...
    def filter_by_year(self, data, year: int): ...
    def filter_by_date_range(self, data, start_year: int, end_year: int): ...

    # ── 8 analysis functions ───────────────────────────────────
    def get_top_10_countries(self, data) -> List[Dict]: ...
    def get_bottom_10_countries(self, data) -> List[Dict]: ...
    def get_gdp_growth_rate(self, data) -> List[Dict]: ...
    def get_average_gdp_by_continent(self, data) -> List[Dict]: ...
    def get_global_gdp_trend(self, data) -> List[Dict]: ...
    def get_fastest_growing_continent(self, data) -> List[Dict]: ...
    def get_declining_countries(self, data, decline_years: int) -> List[Dict]: ...
    def get_continent_contributions(self, data) -> List[Dict]: ...

    # ── entry point (implements PipelineService) ───────────────
    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        # 1. convert to dataframe
        # 2. read config values
        # 3. filter data
        # 4. run all 8 analyses
        # 5. call self.sink.write() — never calls a concrete writer
        ...


# -----------------
#  PLUGINS , inputs  (implement DataReader protocol)
#  Blind to Core internals --- only calls PipelineService.execute()

class JSONReader:
    """Reads GDP data from .json file — implements DataReader"""
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def read(self) -> List[Dict[str, Any]]:
        # load json, reshape wide→long, clean, return list of dicts
        ...


class CSVReader:
    """Reads GDP data from .csv file — implements DataReader"""
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def read(self) -> List[Dict[str, Any]]:
        # load csv, reshape if needed, clean, return list of dicts
        ...


class ExcelReader:
    """Reads GDP data from .xlsx file — implements DataReader"""
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def read(self) -> List[Dict[str, Any]]:
        # load excel, reshape wide→long, clean, return list of dicts
        ...


# ------------------
#  PLUGINS — outputs  (implement DataSink protocol)
#  Core calls write() — never knows which writer is being used

class ConsoleWriter:
    """Prints results to terminal — implements DataSink"""
    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        # print each result to terminal
        ...


class GraphicsChartWriter:
    """Saves 8 charts as PNG files — implements DataSink"""
    def __init__(self, output_dir: str = "output") -> None:
        self.output_dir = output_dir

    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        # read config values from data
        # call all 8 chart methods
        ...

    def _bar_chart(self, data, x_key, y_key, title, xlabel, ylabel, filename, color): ...
    def _horizontal_bar(self, data, x_key, y_key, title, xlabel, ylabel, filename): ...
    def _line_chart(self, data, x_key, y_key, title, xlabel, ylabel, filename): ...
    def _pie_chart(self, data, label_key, value_key, title, filename): ...
    def _declining_chart(self, data, continent, decline_years, filename): ...


class FileWriter:
    """Saves results to .txt file — implements DataSink"""
    def __init__(self, output_dir: str = "output") -> None:
        self.output_dir = output_dir

    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        # write results to results.txt
        ...


# ----------------
#  MAIN — orchestrator
#  its job; read config, wire components, start pipeline


class FactoryRegistry:
    """Maps config strings to actual classes"""
    INPUT_DRIVERS = {
        "json":  JSONReader,
        "csv":   CSVReader,
        "excel": ExcelReader,
    }
    OUTPUT_DRIVERS = {
        "console":  ConsoleWriter,
        "graphics": GraphicsChartWriter,
        "file":     FileWriter,
    }


class Main:
    """Entry point — bootstrap and wire everything"""

    @staticmethod
    def load_config(filepath: str = "config.json") -> dict:
        # open and parse config.json
        ...

    @staticmethod
    def create_input_reader(config: dict) -> DataReader:
        # use FactoryRegistry to pick correct reader
        ...

    @staticmethod
    def create_output_writer(config: dict) -> DataSink:
        # use FactoryRegistry to pick correct writer
        ...

    @staticmethod
    def bootstrap() -> None:
        # 1. load config
        # 2. create output writer  (sink)
        # 3. create engine         (inject sink)
        # 4. create input reader   (inject engine)
        # 5. reader.read() → engine.execute() → sink.write()
        ...

    @staticmethod
    def main() -> None:
        # call bootstrap(), handle exceptions
        ...