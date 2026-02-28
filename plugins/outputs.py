from typing import List, Dict, Any
import matplotlib.pyplot as plt
import os


class ConsoleWriter:
    """
    prints results to terminal
    """

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


# ===============================
# FIZA'S WORK - GRAPHICS WRITER
# ===============================

class GraphicsChartWriter:
    """
    creates charts and saves them to output folder
    """

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print("graphics chart writer initialized")

    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        if not data:
            print("no data received for charts")
            return

        results = data[0]

        config = results.get("config", {})
        continent = config.get("continent", "Unknown")
        year = config.get("year", 2020)
        start_year = config.get("start_year", 2015)
        end_year = config.get("end_year", 2020)

        print(f"creating charts for {continent}")

        self.create_bar_chart(
            results.get("top_10_countries", []),
            f"Top 10 Countries in {continent} ({year})",
            f"top10_{continent}_{year}.png"
        )

        self.create_pie_chart(
            results.get("continent_contributions", []),
            f"Continent Contribution ({start_year}-{end_year})",
            f"contribution_{start_year}_{end_year}.png"
        )

        self.create_line_graph(
            results.get("global_trend", []),
            f"Global GDP Trend ({start_year}-{end_year})",
            f"global_trend_{start_year}_{end_year}.png"
        )

    # ===============================
    # CHART METHODS
    # ===============================

    def create_bar_chart(self, data: List[Dict], title: str, filename: str):
        if not data:
            return

        countries = [item["country"] for item in data]
        values = [item["gdp"] for item in data]

        plt.figure(figsize=(10, 6))
        plt.bar(countries, values, color="green")
        plt.xticks(rotation=45)
        plt.title(title)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()

        print(f"saved {filename}")

    def create_pie_chart(self, data: List[Dict], title: str, filename: str):
        if not data:
            return

        continents = [item["continent"] for item in data]
        values = [item["contribution_percent"] for item in data]

        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=continents, autopct="%1.1f%%")
        plt.title(title)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()

        print(f"saved {filename}")

    def create_line_graph(self, data: List[Dict], title: str, filename: str):
        if not data:
            return

        years = [item["year"] for item in data]
        values = [item["total_global_gdp"] for item in data]

        plt.figure(figsize=(10, 6))
        plt.plot(years, values, marker="o")
        plt.title(title)
        plt.xlabel("Year")
        plt.ylabel("Global GDP")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()

        print(f"saved {filename}")


# ===============================
# OPTIONAL FILE WRITER
# ===============================

class FileWriter:
    """
    saves results to a text file
    """

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        filepath = os.path.join(self.output_dir, "results.txt")

        with open(filepath, "w", encoding="utf-8") as f:
            if title:
                f.write(title + "\n\n")

            for item in data:
                for key, value in item.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")

        print("results saved to results.txt")