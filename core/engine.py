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
        """filter data by region or continent"""
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
        """filter data by specific year"""
        print(f"filtering by year {year}")
        filtered = data[data['Year'] == year]
        print(f"found {len(filtered)} rows for year {year}")
        return filtered


    def filter_by_date_range(self, data: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
        """filter data by year range"""
        print(f"filtering by date range {start_year} to {end_year}")
        filtered = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
        print(f"found {len(filtered)} rows in range")
        return filtered


    # ─────────────────────────────────────────────────────────────
    # FIZA'S 8 ANALYSIS FUNCTIONS
    # ─────────────────────────────────────────────────────────────

    def calculate_top_10_countries(self, data: pd.DataFrame, year: int) -> List[Dict[str, Any]]:
        """find top 10 countries by gdp for specific year"""
        year_data = data[data['Year'] == year]
        top_10 = year_data.nlargest(10, 'Value')
        result = []
        for _, row in top_10.iterrows():
            result.append({
                'country': row['Country Name'],
                'gdp': row['Value'],
                'year': row['Year']
            })
        return result


    def calculate_bottom_10_countries(self, data: pd.DataFrame, year: int) -> List[Dict[str, Any]]:
        """find bottom 10 countries by gdp for specific year"""
        year_data = data[data['Year'] == year]
        bottom_10 = year_data.nsmallest(10, 'Value')
        result = []
        for _, row in bottom_10.iterrows():
            result.append({
                'country': row['Country Name'],
                'gdp': row['Value'],
                'year': row['Year']
            })
        return result


    def calculate_gdp_growth_rate(self, data: pd.DataFrame, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        """calculate gdp growth rate for each country between two years"""
        result = []
        for country in data['Country Name'].unique():
            cd = data[data['Country Name'] == country]
            s = cd[cd['Year'] == start_year]['Value']
            e = cd[cd['Year'] == end_year]['Value']
            if len(s) > 0 and len(e) > 0 and s.values[0] > 0:
                rate = ((e.values[0] - s.values[0]) / s.values[0]) * 100
                result.append({
                    'country': country,
                    'start_year': start_year,
                    'end_year': end_year,
                    'growth_rate': round(rate, 2)
                })
        result.sort(key=lambda x: x['growth_rate'], reverse=True)
        return result


    def calculate_average_by_continent(self, data: pd.DataFrame, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        """calculate average gdp by continent for date range"""
        rd = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
        result = []
        for region, avg in rd.groupby('Region')['Value'].mean().items():
            result.append({
                'continent': region,
                'average_gdp': round(avg, 2),
                'start_year': start_year,
                'end_year': end_year
            })
        result.sort(key=lambda x: x['average_gdp'], reverse=True)
        return result


    def calculate_global_gdp_trend(self, data: pd.DataFrame, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        """calculate total global gdp trend over years"""
        real = data[data['Region'] != 'Global'] if 'Global' in data['Region'].values else data
        rd = real[(real['Year'] >= start_year) & (real['Year'] <= end_year)]
        result = []
        for year, total in rd.groupby('Year')['Value'].sum().items():
            result.append({'year': int(year), 'total_global_gdp': round(total, 2)})
        result.sort(key=lambda x: x['year'])
        return result


    def calculate_fastest_growing_continent(self, data: pd.DataFrame, start_year: int, end_year: int) -> Dict[str, Any]:
        """find which continent had fastest gdp growth"""
        real = data[data['Region'] != 'Global'] if 'Global' in data['Region'].values else data
        rates = []
        for region in real['Region'].unique():
            rd = real[real['Region'] == region]
            s = rd[rd['Year'] == start_year]['Value'].sum()
            e = rd[rd['Year'] == end_year]['Value'].sum()
            if s > 0:
                rates.append({
                    'continent': region,
                    'start_year': start_year,
                    'end_year': end_year,
                    'start_gdp': round(s, 2),
                    'end_gdp': round(e, 2),
                    'growth_rate': round(((e - s) / s) * 100, 2)
                })
        return max(rates, key=lambda x: x['growth_rate']) if rates else {}


    def find_declining_countries(self, data: pd.DataFrame, years: int) -> List[Dict[str, Any]]:
        """find countries with consistent gdp decline over last x years"""
        max_yr = int(data['Year'].max())
        min_yr = max_yr - years + 1
        recent = data[(data['Year'] >= min_yr) & (data['Year'] <= max_yr)]
        declining = []
        for country in recent['Country Name'].unique():
            cd = recent[recent['Country Name'] == country].sort_values('Year')
            if len(cd) >= years:
                vals = cd['Value'].values
                if all(vals[i] < vals[i - 1] for i in range(1, len(vals))):
                    pct = ((vals[-1] - vals[0]) / vals[0]) * 100
                    declining.append({
                        'country': country,
                        'start_year': int(cd['Year'].min()),
                        'end_year': int(cd['Year'].max()),
                        'decline_percent': round(pct, 2)
                    })
        return declining


    def calculate_continent_contribution(self, data: pd.DataFrame, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        """calculate each continents contribution to global gdp percentage"""
        real = data[data['Region'] != 'Global'] if 'Global' in data['Region'].values else data
        rd = real[(real['Year'] >= start_year) & (real['Year'] <= end_year)]
        totals = rd.groupby('Region')['Value'].sum()
        global_total = totals.sum()
        result = []
        for cont, total in totals.items():
            result.append({
                'continent': cont,
                'total_gdp': round(total, 2),
                'contribution_percent': round((total / global_total) * 100, 2),
                'start_year': start_year,
                'end_year': end_year
            })
        result.sort(key=lambda x: x['contribution_percent'], reverse=True)
        return result


    # ─────────────────────────────────────────────────────────────
    # execute() — main method called by the Input reader
    # ─────────────────────────────────────────────────────────────

    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        """
        main execution method
        processes raw data and sends to output
        args:
            raw_data list of gdp records from input reader
        """
        print("\n" + "=" * 60)
        print("starting gdp analysis")
        print("=" * 60)

        # convert to dataframe
        self.data = pd.DataFrame(raw_data)
        print(f"loaded {len(self.data)} total records")

        # get configuration
        analysis_config = self.config.get('analysis', {})
        continent    = analysis_config.get('continent', 'Asia')
        year         = analysis_config.get('year', 2020)
        start_year   = analysis_config.get('start_year', 2015)
        end_year     = analysis_config.get('end_year', 2020)
        decline_years = analysis_config.get('decline_years', 3)

        print("\nanalysis configuration")
        print(f"continent {continent}")
        print(f"year {year}")
        print(f"date range {start_year} to {end_year}")

        # filter data
        continent_data = self.filter_by_region(self.data, continent)
        range_data     = self.filter_by_date_range(self.data, start_year, end_year)

        # ── FIZA'S 8 ANALYSIS CALLS ───────────────────────────────
        print("\nrunning analysis functions...")

        top_10       = self.calculate_top_10_countries(continent_data, year)
        bottom_10    = self.calculate_bottom_10_countries(continent_data, year)
        growth_rates = self.calculate_gdp_growth_rate(continent_data, start_year, end_year)
        cont_avgs    = self.calculate_average_by_continent(range_data, start_year, end_year)
        global_trend = self.calculate_global_gdp_trend(self.data, start_year, end_year)
        fastest      = self.calculate_fastest_growing_continent(self.data, start_year, end_year)
        declining    = self.find_declining_countries(continent_data, decline_years)
        contributions = self.calculate_continent_contribution(self.data, start_year, end_year)

        print("all 8 analyses complete")

        # bundle all results
        all_results = {
            'config': {
                'continent':     continent,
                'year':          year,
                'start_year':    start_year,
                'end_year':      end_year,
                'decline_years': decline_years,
            },
            'top_10_countries':           top_10,
            'bottom_10_countries':        bottom_10,
            'growth_rates':               growth_rates[:20],
            'continent_averages':         cont_avgs,
            'global_trend':               global_trend,
            'fastest_growing_continent':  fastest,
            'declining_countries':        declining,
            'continent_contributions':    contributions,
        }

        print("\n" + "=" * 60)
        print("analysis complete")
        print("=" * 60)

        # send results to output (via injected DataSink)
        self.sink.write([all_results], f"gdp analysis for {continent}")

        print("\nresults sent to output")
