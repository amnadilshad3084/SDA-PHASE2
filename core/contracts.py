"""
contracts module defines protocols interfaces (like a rule book)
"""
from typing import Protocol, List, Dict, Any
from typing_extensions import runtime_checkable

@runtime_checkable
class DataSink(Protocol):
    """
    to write output graphs console file
    """
    
    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        """
        to display results
        args:
            data results to display
            title title for output
        """
        ...


@runtime_checkable
class PipelineService(Protocol):
    """
    protocol for core engine
    input files send data to execute function
    """
    
    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        """
        process raw data
        args:
            raw_data gdp data from input file
        """
        ...


@runtime_checkable
class DataReader(Protocol):
    """
    protocol for input readers
    reads json csv excel files
    """
    
    def read(self) -> List[Dict[str, Any]]:
        """
        read data from source
        returns:
            list of gdp data records
        """
        ...