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
    handles filtering and all required analyses
    """

    def __init__(self, sink: DataSink, config: dict):
        self.sink = sink
        self.config = config
        self.data = None
        print("transformation engine initialized")


    def filter_by_region(self, data: pd.DataFrame, region: str) -> pd.DataFrame:
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
        filtered = data[data['Year'] == year]
        print(f"found {len(filtered)} rows for year {year}")
        return filtered


    def filter_by_date_range(self, data: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
        filtered = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
        print(f"found {len(filtered)} rows in range {start_year}-{end_year}")
        return filtered


    # 1. Top 10 countries by GDP
    def get_top_10_countries(self, data: pd.DataFrame) -> List[Dict]:
        result = (
            data.groupby('Country Name')['Value']
            .mean()
            .nlargest(10)
            .reset_index()
        )
        return list(map(
            lambda row: {"country": row["Country Name"], "gdp": round(row["Value"], 2)},
            result.to_dict('records')
        ))


    # 2. Bottom 10 countries by GDP 
    def get_bottom_10_countries(self, data: pd.DataFrame) -> List[Dict]:
        result = (
            data.groupby('Country Name')['Value']
            .mean()
            .nsmallest(10)
            .reset_index()
        )
        return list(map(
            lambda row: {"country": row["Country Name"], "gdp": round(row["Value"], 2)},
            result.to_dict('records')
        ))


    # 3. GDP growth rate per country 
    def get_gdp_growth_rate(self, data: pd.DataFrame) -> List[Dict]:
        growth_list = []
        for country, group in data.groupby('Country Name'):
            group = group.sort_values('Year')
            if len(group) >= 2:
                first_gdp = group.iloc[0]['Value']
                last_gdp  = group.iloc[-1]['Value']
                if first_gdp and first_gdp != 0:
                    growth = ((last_gdp - first_gdp) / first_gdp) * 100
                    growth_list.append({
                        "country": country,
                        "growth_rate": round(growth, 2)
                    })
        # sort descending using lambda
        return sorted(growth_list, key=lambda x: x["growth_rate"], reverse=True)


    # 4. Average GDP by continent 
    def get_average_gdp_by_continent(self, data: pd.DataFrame) -> List[Dict]:
        region_col = 'Region' if 'Region' in data.columns else 'Continent'
        result = (
            data.groupby(region_col)['Value']
            .mean()
            .reset_index()
        )
        return list(map(
            lambda row: {"continent": row[region_col], "avg_gdp": round(row["Value"], 2)},
            result.to_dict('records')
        ))


    # 5. Total global GDP trend
    def get_global_gdp_trend(self, data: pd.DataFrame) -> List[Dict]:
        result = (
            data.groupby('Year')['Value']
            .sum()
            .reset_index()
        )
        return list(map(
            lambda row: {"year": int(row["Year"]), "total_global_gdp": round(row["Value"], 2)},
            result.to_dict('records')
        ))


    # 6. Fastest growing continent
    def get_fastest_growing_continent(self, data: pd.DataFrame) -> List[Dict]:
        region_col = 'Region' if 'Region' in data.columns else 'Continent'
        growth_list = []
        for continent, group in data.groupby(region_col):
            yearly = group.groupby('Year')['Value'].sum().sort_index()
            if len(yearly) >= 2:
                first = yearly.iloc[0]
                last  = yearly.iloc[-1]
                if first and first != 0:
                    growth = ((last - first) / first) * 100
                    growth_list.append({
                        "continent": continent,
                        "growth_rate": round(growth, 2)
                    })
        return sorted(growth_list, key=lambda x: x["growth_rate"], reverse=True)


    # 7. Countries with consistent GDP decline 
    def get_declining_countries(self, data: pd.DataFrame, decline_years: int) -> List[Dict]:
        declining = []
        for country, group in data.groupby('Country Name'):
            group = group.sort_values('Year').tail(decline_years + 1)
            values = list(group['Value'])
            # check if each year is less than previous using all() + zip + lambda
            if len(values) > decline_years:
                is_declining = all(map(lambda pair: pair[1] < pair[0], zip(values, values[1:])))
                if is_declining:
                    declining.append({"country": country})
        return declining


    # 8. Contribution of each continent to global GDP
    def get_continent_contributions(self, data: pd.DataFrame) -> List[Dict]:
        region_col = 'Region' if 'Region' in data.columns else 'Continent'
        continent_gdp = data.groupby(region_col)['Value'].sum()
        total = continent_gdp.sum()
        result = continent_gdp.reset_index()
        return list(map(
            lambda row: {
                "continent": row[region_col],
                "contribution_percent": round((row["Value"] / total) * 100, 2)
            },
            result.to_dict('records')
        ))


    #  main execute 
    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        print("\n" + "="*60)
        print("starting gdp analysis")
        print("="*60)

        self.data = pd.DataFrame(raw_data)
        print(f"loaded {len(self.data)} total records")

        analysis_config = self.config.get('analysis', {})
        continent    = analysis_config.get('continent',    'Asia')
        year         = analysis_config.get('year',         2020)
        start_year   = analysis_config.get('start_year',   2015)
        end_year     = analysis_config.get('end_year',     2020)
        decline_years= analysis_config.get('decline_years', 3)

        # these are filtered views
        continent_data = self.filter_by_region(self.data, continent)
        year_data      = self.filter_by_year(continent_data, year)
        range_data     = self.filter_by_date_range(self.data, start_year, end_year)
        cont_range     = self.filter_by_date_range(continent_data, start_year, end_year)

        print("\nrunning all analyses...")

        results = {
            "config": {
                "continent":    continent,
                "year":         year,
                "start_year":   start_year,
                "end_year":     end_year,
                "decline_years": decline_years
            },
            "top_10_countries":        self.get_top_10_countries(year_data),
            "bottom_10_countries":     self.get_bottom_10_countries(year_data),
            "gdp_growth_rate":         self.get_gdp_growth_rate(cont_range),
            "avg_gdp_by_continent":    self.get_average_gdp_by_continent(range_data),
            "global_trend":            self.get_global_gdp_trend(range_data),
            "fastest_growing":         self.get_fastest_growing_continent(range_data),
            "declining_countries":     self.get_declining_countries(continent_data, decline_years),
            "continent_contributions": self.get_continent_contributions(range_data),
        }

        print("all analyses complete, sending to output")
        self.sink.write([results], f"GDP Analysis — {continent} ({year})")