"""
output module - writes results to console or charts
"""
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')   # saves files without display window
import os


class ConsoleWriter:
    """prints results to terminal"""

    def __init__(self):
        print("console writer initialized")

    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        print("\n" + "="*60)
        if title:
            print(title)
            print("="*60)
        for item in data:
            for key, value in item.items():
                print(f"{key}: {value}")
        print("="*60)



#  GRAPHICS CHART WRITER  (all 8 charts)

class GraphicsChartWriter:
    """creates and saves all required charts to output/ folder"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        print(f"graphics chart writer initialized → saving to '{output_dir}/'")

    #  entry point called by engine 
    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        if not data:
            print("no data received for charts")
            return

        results  = data[0]
        config   = results.get("config", {})
        continent  = config.get("continent",  "Unknown")
        year       = config.get("year",       2020)
        start_year = config.get("start_year", 2015)
        end_year   = config.get("end_year",   2020)

        print(f"\ncreating all charts for {continent} ...")

        # 1. Top 10 countries bar chart
        self._bar_chart(
            results.get("top_10_countries", []),
            "country", "gdp",
            f"Top 10 Countries by GDP — {continent} ({year})",
            "Country", "GDP (USD)",
            f"1_top10_{continent}_{year}.png",
            color="#2196F3"
        )

        # 2. Bottom 10 countries bar chart
        self._bar_chart(
            results.get("bottom_10_countries", []),
            "country", "gdp",
            f"Bottom 10 Countries by GDP — {continent} ({year})",
            "Country", "GDP (USD)",
            f"2_bottom10_{continent}_{year}.png",
            color="#F44336"
        )

        # 3. GDP growth rate horizontal bar
        self._horizontal_bar(
            results.get("gdp_growth_rate", [])[:15],   # top 15
            "country", "growth_rate",
            f"GDP Growth Rate — {continent} ({start_year}–{end_year})",
            "Growth Rate (%)", "Country",
            f"3_growth_rate_{continent}.png"
        )

        # 4. Average GDP by continent bar chart
        self._bar_chart(
            results.get("avg_gdp_by_continent", []),
            "continent", "avg_gdp",
            f"Average GDP by Continent ({start_year}–{end_year})",
            "Continent", "Average GDP (USD)",
            f"4_avg_gdp_by_continent.png",
            color="#4CAF50"
        )

        # 5. Global GDP trend line chart
        self._line_chart(
            results.get("global_trend", []),
            "year", "total_global_gdp",
            f"Total Global GDP Trend ({start_year}–{end_year})",
            "Year", "Total Global GDP (USD)",
            f"5_global_trend.png"
        )

        # 6. Fastest growing continent bar chart
        self._bar_chart(
            results.get("fastest_growing", []),
            "continent", "growth_rate",
            f"Fastest Growing Continents ({start_year}–{end_year})",
            "Continent", "Growth Rate (%)",
            f"6_fastest_growing.png",
            color="#FF9800"
        )

        # 7. Declining countries — just show count as text chart
        declining = results.get("declining_countries", [])
        self._declining_chart(
            declining,
            continent,
            config.get("decline_years", 3),
            f"7_declining_{continent}.png"
        )

        # 8. Continent contribution pie chart
        self._pie_chart(
            results.get("continent_contributions", []),
            "continent", "contribution_percent",
            f"Continent Contribution to Global GDP ({start_year}–{end_year})",
            f"8_contribution_{start_year}_{end_year}.png"
        )

        print(f"\n{'='*60}")
        print(f"ALL CHARTS SAVED TO: {os.path.abspath(self.output_dir)}/")
        print(f"{'='*60}")
        print("Open VS Code Explorer → output folder → click any .png to view")

    # ── individual chart helpers ────────────────────────────────────────────

    def _bar_chart(self, data, x_key, y_key, title, xlabel, ylabel, filename, color="#2196F3"):
        if not data:
            print(f"skipping {filename} — no data")
            return
        labels = [str(item[x_key]) for item in data]
        values = [item[y_key] for item in data]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(labels, values, color=color, edgecolor='white')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"  saved → {filename}")

    def _horizontal_bar(self, data, x_key, y_key, title, xlabel, ylabel, filename):
        if not data:
            print(f"skipping {filename} — no data")
            return
        labels = [str(item[x_key]) for item in data]
        values = [item[y_key] for item in data]
        colors = list(map(lambda v: "#4CAF50" if v >= 0 else "#F44336", values))

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(labels, values, color=colors)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.axvline(0, color='black', linewidth=0.8)
        plt.tight_layout()
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"  saved → {filename}")

    def _line_chart(self, data, x_key, y_key, title, xlabel, ylabel, filename):
        if not data:
            print(f"skipping {filename} — no data")
            return
        xs = [item[x_key] for item in data]
        ys = [item[y_key] for item in data]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(xs, ys, marker='o', color="#9C27B0", linewidth=2, markersize=6)
        ax.fill_between(xs, ys, alpha=0.15, color="#9C27B0")
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"  saved → {filename}")

    def _pie_chart(self, data, label_key, value_key, title, filename):
        if not data:
            print(f"skipping {filename} — no data")
            return
        labels = [str(item[label_key]) for item in data]
        values = [item[value_key] for item in data]

        fig, ax = plt.subplots(figsize=(9, 9))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        plt.tight_layout()
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"  saved → {filename}")

    def _declining_chart(self, data, continent, decline_years, filename):
        names = [item["country"] for item in data] if data else ["None found"]
        text  = "\n".join(names) if names else "None"

        fig, ax = plt.subplots(figsize=(8, max(4, len(names) * 0.4 + 2)))
        ax.axis('off')
        ax.set_title(
            f"Countries with Consistent GDP Decline\n(Last {decline_years} years — {continent})",
            fontsize=14, fontweight='bold', pad=15
        )
        ax.text(
            0.5, 0.5, text,
            ha='center', va='center',
            fontsize=11, transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#FFECB3', alpha=0.8)
        )
        plt.tight_layout()
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"  saved → {filename}")


# ─────────────────────────────────────────────
#  FILE WRITER (optional bonus)
# ─────────────────────────────────────────────
class FileWriter:
    """saves results as text file"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        filepath = os.path.join(self.output_dir, "results.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            if title:
                f.write(title + "\n\n")
            for item in data:
                for key, value in item.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")
        print(f"results saved to {filepath}")