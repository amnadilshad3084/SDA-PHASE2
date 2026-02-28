"""
transformation engine module
contains core business logic for gdp analysis
"""
import pandas as pd
from typing import List, Dict, Any
from core.contracts import DataSink


class TransformationEngine:
    """
    core engine for gdp data processing
    handles filtering and analysis
    """
    
    def __init__(self, sink: DataSink, config: dict):
        """
        initialize engine
        args:
            sink output writer follows datasink protocol
            config configuration dictionary
        """
        self.sink = sink
        self.config = config
        self.data = None
        print("transformation engine initialized")
    
    
    def filter_by_region(self, data: pd.DataFrame, region: str) -> pd.DataFrame:
        """
        filter data by region or continent
        args:
            data gdp dataframe
            region region name to filter
        returns:
            filtered dataframe
        """
        print(f"filtering by region {region}")
        
        if 'Region' in data.columns:
            filtered = data[data['Region'] == region]
        elif 'Continent' in data.columns:
            filtered = data[data['Continent'] == region]
        else:
            print("warning no region or continent column found")
            return data
        
        print(f"found {len(filtered)} rows for {region}")
        return filtered
    
    
    def filter_by_year(self, data: pd.DataFrame, year: int) -> pd.DataFrame:
        """
        filter data by specific year
        args:
            data gdp dataframe
            year year to filter
        returns:
            filtered dataframe
        """
        print(f"filtering by year {year}")
        filtered = data[data['Year'] == year]
        print(f"found {len(filtered)} rows for year {year}")
        return filtered
    
    
    def filter_by_date_range(self, data: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
        """
        filter data by year range
        args:
            data gdp dataframe
            start_year starting year
            end_year ending year
        returns:
            filtered dataframe
        """
        print(f"filtering by date range {start_year} to {end_year}")
        filtered = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
        print(f"found {len(filtered)} rows in range")
        return filtered
    
    
    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        """
        main execution method
        processes raw data and sends to output
        args:
            raw_data list of gdp records from input reader
        """
        print("\n" + "="*60)
        print("starting gdp analysis")
        print("="*60)
        
        # convert to dataframe
        self.data = pd.DataFrame(raw_data)
        print(f"loaded {len(self.data)} total records")
        
        # get configuration
        analysis_config = self.config.get('analysis', {})
        continent = analysis_config.get('continent', 'Asia')
        year = analysis_config.get('year', 2020)
        start_year = analysis_config.get('start_year', 2015)
        end_year = analysis_config.get('end_year', 2020)
        decline_years = analysis_config.get('decline_years', 3)
        
        #filter data
        continent_data = self.filter_by_region(self.data, continent)
        year_data = self.filter_by_year(continent_data, year)
        range_data = self.filter_by_date_range(self.data, start_year, end_year)
        
        # results dictionary
        results = {
            'continent': continent,
            'year': year,
            'start_year': start_year,
            'end_year': end_year,
            'total_records': len(self.data),
            'continent_records': len(continent_data),
            'year_records': len(year_data)
        }
        
        print("\nanalysis configuration")
        print(f"continent {continent}")
        print(f"year {year}")
        print(f"date range {start_year} to {end_year}")
        
        # # FIZA'S WORK
        # will add analysis functions here
        # for now just send basic results to output
        
        print("\n" + "="*60)
        print("analysis complete")
        print("="*60)
        
        # send results to output
        self.sink.write([results], f"gdp analysis for {continent}")
        
        print("\nresults sent to output")


                        # FIZA'S WORK
# please add these analysis functions
# 1 calculate_top_10_countries
# 2 calculate_bottom_10_countries
# 3 calculate_gdp_growth_rate
# 4 calculate_average_by_continent
# 5 calculate_global_gdp_trend
# 6 calculate_fastest_growing_continent
# 7 find_declining_countries
# 8 calculate_continent_contribution