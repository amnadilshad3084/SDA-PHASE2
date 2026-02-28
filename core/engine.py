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
    # ==============================
# FIZA'S ANALYSIS FUNCTIONS
# ==============================

def calculate_top_10_countries(self, data, year):
    year_data = data[data['Year'] == year]
    top_10 = year_data.nlargest(10, 'Value')
    return [
        {'country': row['Country Name'], 'gdp': row['Value'], 'year': row['Year']}
        for _, row in top_10.iterrows()
    ]


def calculate_bottom_10_countries(self, data, year):
    year_data = data[data['Year'] == year]
    bottom_10 = year_data.nsmallest(10, 'Value')
    return [
        {'country': row['Country Name'], 'gdp': row['Value'], 'year': row['Year']}
        for _, row in bottom_10.iterrows()
    ]


def calculate_gdp_growth_rate(self, data, start_year, end_year):
    result = []
    countries = data['Country Name'].unique()

    for country in countries:
        country_data = data[data['Country Name'] == country]
        start = country_data[country_data['Year'] == start_year]['Value']
        end = country_data[country_data['Year'] == end_year]['Value']

        if len(start) and len(end):
            start_val = start.values[0]
            end_val = end.values[0]

            if start_val > 0:
                growth = ((end_val - start_val) / start_val) * 100
                result.append({
                    'country': country,
                    'growth_rate': growth
                })

    result.sort(key=lambda x: x['growth_rate'], reverse=True)
    return result


def calculate_average_by_continent(self, data, start_year, end_year):
    range_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
    grouped = range_data.groupby('Region')['Value'].mean()

    return [
        {'continent': region, 'average_gdp': avg}
        for region, avg in grouped.items()
    ]


def calculate_global_gdp_trend(self, data, start_year, end_year):
    range_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
    yearly = range_data.groupby('Year')['Value'].sum()

    return [
        {'year': year, 'total_global_gdp': total}
        for year, total in yearly.items()
    ]


def calculate_fastest_growing_continent(self, data, start_year, end_year):
    regions = data['Region'].unique()
    best = None
    max_growth = float('-inf')

    for region in regions:
        region_data = data[data['Region'] == region]
        start = region_data[region_data['Year'] == start_year]['Value'].sum()
        end = region_data[region_data['Year'] == end_year]['Value'].sum()

        if start > 0:
            growth = ((end - start) / start) * 100
            if growth > max_growth:
                max_growth = growth
                best = {
                    'continent': region,
                    'growth_rate': growth
                }

    return best


def find_declining_countries(self, data, years):
    max_year = data['Year'].max()
    min_year = max_year - years + 1
    recent = data[(data['Year'] >= min_year)]

    declining = []

    for country in recent['Country Name'].unique():
        c_data = recent[recent['Country Name'] == country].sort_values('Year')
        values = c_data['Value'].values

        if len(values) >= years and all(values[i] < values[i-1] for i in range(1, len(values))):
            decline_percent = ((values[-1] - values[0]) / values[0]) * 100
            declining.append({
                'country': country,
                'decline_percent': decline_percent
            })

    return declining


def calculate_continent_contribution(self, data, start_year, end_year):
    range_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
    totals = range_data.groupby('Region')['Value'].sum()
    global_total = totals.sum()

    return [
        {
            'continent': region,
            'contribution_percent': (value / global_total) * 100
        }
        for region, value in totals.items()
    ]
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
