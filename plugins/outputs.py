"""
plugins/outputs.py
Output implementations: ConsoleWriter and GraphicsChartWriter
Satisfies the DataSink Protocol defined in core/contracts.py
Fiza's work: Full implementation of both writers
"""

from typing import List, Dict, Any
import os


# ═══════════════════════════════════════════════════════════════════════
# ConsoleWriter — prints results to terminal
# ═══════════════════════════════════════════════════════════════════════
class ConsoleWriter:
    """Simple writer that prints all results to the console."""

    def __init__(self):
        print("ConsoleWriter initialized ✓")

    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        """Print analysis results to stdout."""
        print("\n" + "=" * 60)
        if title:
            print(f"  {title}")
            print("=" * 60)

        if not data:
            print("  No data to display.")
            return

        results = data[0]
        cfg = results.get("config", {})
        continent = cfg.get("continent", "N/A")
        year      = cfg.get("year", "N/A")

        print(f"\n  Continent : {continent}  |  Year : {year}")
        print(f"  Range     : {cfg.get('start_year')} – {cfg.get('end_year')}")
        print()

        def _fmt(v):
            if isinstance(v, float):
                return f"{v:,.2f}"
            return str(v)

        for key, value in results.items():
            if key == "config":
                continue
            print(f"  ── {key.replace('_', ' ').upper()} ──")
            if isinstance(value, list):
                for item in value[:5]:
                    print("    ", {k: _fmt(v) for k, v in item.items()})
                if len(value) > 5:
                    print(f"    … and {len(value) - 5} more")
            elif isinstance(value, dict):
                for k, v in value.items():
                    print(f"    {k}: {_fmt(v)}")
            else:
                print(f"    {_fmt(value)}")
            print()

        print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════
# GraphicsChartWriter — saves all 8 charts to disk
# ═══════════════════════════════════════════════════════════════════════
class GraphicsChartWriter:
    """Creates detailed, publication-quality charts for all 8 GDP analyses."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        print(f"GraphicsChartWriter initialized — output dir: '{output_dir}' ✓")

    # ── Main entry point ────────────────────────────────────────────────
    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        """
        Receives the bundled analysis results dict and creates all charts.
        CRITICAL: Every title / filename uses values from config — never hardcoded.
        """
        import matplotlib
        matplotlib.use("Agg")   # non-interactive backend (safe for all environments)
        import matplotlib.pyplot as plt

        if not data:
            print("GraphicsChartWriter: no data received.")
            return

        results   = data[0]
        config    = results.get("config", {})

        # ── Read ALL parameters from config (never hardcode) ────────────
        continent     = config.get("continent", "Unknown")
        year          = config.get("year", 2020)
        start_year    = config.get("start_year", 2015)
        end_year      = config.get("end_year", 2020)

        print(f"\nCreating charts for: {continent} | {year} | {start_year}–{end_year}")
        print("-" * 50)

        self._chart_top10(
            results.get("top_10_countries", []),
            continent, year, plt
        )
        self._chart_bottom10(
            results.get("bottom_10_countries", []),
            continent, year, plt
        )
        self._chart_growth_rate(
            results.get("growth_rates", []),
            continent, start_year, end_year, plt
        )
        self._chart_continent_average(
            results.get("continent_averages", []),
            start_year, end_year, plt
        )
        self._chart_global_trend(
            results.get("global_trend", []),
            start_year, end_year, plt
        )
        self._chart_fastest_growing(
            results.get("fastest_growing_continent", {}),
            start_year, end_year, plt
        )
        self._chart_declining_countries(
            results.get("declining_countries", []),
            continent, plt
        )
        self._chart_contribution_pie(
            results.get("continent_contributions", []),
            start_year, end_year, plt
        )

        print(f"\nAll 8 charts saved to '{self.output_dir}/' ✓")

    # ── Helper: save figure ──────────────────────────────────────────────
    def _save(self, plt, filename: str) -> None:
        import os
        path = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved: {filename}")

    # ── Chart 1: Top 10 Countries ────────────────────────────────────────
    def _chart_top10(self, data, continent: str, year: int, plt) -> None:
        if not data:
            print("  Skipped top-10 (no data)")
            return

        countries  = [d["country"] for d in data]
        gdp_values = [d["gdp"] / 1e9 for d in data]   # → billions

        fig, ax = plt.subplots(figsize=(14, 7))
        bars = ax.barh(countries[::-1], gdp_values[::-1],
                       color="steelblue", edgecolor="navy", linewidth=0.8)

        # value labels
        for bar, val in zip(bars, gdp_values[::-1]):
            ax.text(bar.get_width() + max(gdp_values) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"${val:,.1f}B",
                    va="center", fontsize=9)

        ax.set_title(f"Top 10 Countries by GDP in {continent} ({year})",
                     fontsize=16, fontweight="bold", pad=15)
        ax.set_xlabel("GDP (Billions USD)", fontsize=12)
        ax.set_ylabel("Country", fontsize=12)
        ax.grid(axis="x", alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fname = f"1_top10_countries_{continent.replace(' ', '_')}_{year}.png"
        self._save(plt, fname)

    # ── Chart 2: Bottom 10 Countries ────────────────────────────────────
    def _chart_bottom10(self, data, continent: str, year: int, plt) -> None:
        if not data:
            print("  Skipped bottom-10 (no data)")
            return

        countries  = [d["country"] for d in data]
        gdp_values = [d["gdp"] / 1e6 for d in data]   # → millions

        fig, ax = plt.subplots(figsize=(14, 7))
        bars = ax.barh(countries[::-1], gdp_values[::-1],
                       color="tomato", edgecolor="darkred", linewidth=0.8)

        for bar, val in zip(bars, gdp_values[::-1]):
            ax.text(bar.get_width() + max(gdp_values) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"${val:,.1f}M",
                    va="center", fontsize=9)

        ax.set_title(f"Bottom 10 Countries by GDP in {continent} ({year})",
                     fontsize=16, fontweight="bold", pad=15)
        ax.set_xlabel("GDP (Millions USD)", fontsize=12)
        ax.set_ylabel("Country", fontsize=12)
        ax.grid(axis="x", alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fname = f"2_bottom10_countries_{continent.replace(' ', '_')}_{year}.png"
        self._save(plt, fname)

    # ── Chart 3: GDP Growth Rate ─────────────────────────────────────────
    def _chart_growth_rate(self, data, continent: str,
                           start_year: int, end_year: int, plt) -> None:
        if not data:
            print("  Skipped growth-rate (no data)")
            return

        # show top 15 + bottom 5 for readability
        top15    = data[:15]
        bottom5  = data[-5:]
        display  = top15 + [d for d in bottom5 if d not in top15]

        countries = [d["country"] for d in display]
        rates     = [d["growth_rate"] for d in display]
        colors    = ["#2ecc71" if r >= 0 else "#e74c3c" for r in rates]

        fig, ax = plt.subplots(figsize=(16, 8))
        ax.bar(countries, rates, color=colors, edgecolor="black", linewidth=0.5)
        ax.axhline(0, color="black", linewidth=0.8)

        for i, (c, r) in enumerate(zip(countries, rates)):
            va = "bottom" if r >= 0 else "top"
            offset = 0.5 if r >= 0 else -0.5
            ax.text(i, r + offset, f"{r:.1f}%", ha="center",
                    va=va, fontsize=7.5, fontweight="bold")

        ax.set_title(
            f"GDP Growth Rate in {continent} ({start_year}–{end_year})\n"
            "Green = Growth  |  Red = Decline",
            fontsize=15, fontweight="bold", pad=15,
        )
        ax.set_xlabel("Country", fontsize=12)
        ax.set_ylabel("Growth Rate (%)", fontsize=12)
        ax.set_xticklabels(countries, rotation=45, ha="right", fontsize=8)
        ax.grid(axis="y", alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fname = (f"3_growth_rate_{continent.replace(' ', '_')}"
                 f"_{start_year}_{end_year}.png")
        self._save(plt, fname)

    # ── Chart 4: Average GDP by Continent ────────────────────────────────
    def _chart_continent_average(self, data, start_year: int, end_year: int, plt) -> None:
        if not data:
            print("  Skipped continent-average (no data)")
            return

        continents = [d["continent"] for d in data]
        averages   = [d["average_gdp"] / 1e9 for d in data]

        colors = plt.cm.tab10.colors[: len(continents)]
        fig, ax = plt.subplots(figsize=(12, 7))
        bars = ax.bar(continents, averages, color=colors, edgecolor="black", linewidth=0.6)

        for bar, val in zip(bars, averages):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(averages) * 0.01,
                    f"${val:,.1f}B", ha="center", va="bottom", fontsize=9)

        ax.set_title(f"Average GDP by Continent ({start_year}–{end_year})",
                     fontsize=16, fontweight="bold", pad=15)
        ax.set_xlabel("Continent", fontsize=12)
        ax.set_ylabel("Average GDP (Billions USD)", fontsize=12)
        ax.set_xticklabels(continents, rotation=30, ha="right")
        ax.grid(axis="y", alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fname = f"4_continent_avg_gdp_{start_year}_{end_year}.png"
        self._save(plt, fname)

    # ── Chart 5: Global GDP Trend ─────────────────────────────────────────
    def _chart_global_trend(self, data, start_year: int, end_year: int, plt) -> None:
        if not data:
            print("  Skipped global-trend (no data)")
            return

        years      = [d["year"] for d in data]
        gdp_values = [d["total_global_gdp"] / 1e12 for d in data]   # → trillions

        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(years, gdp_values, marker="o", linewidth=2.5,
                markersize=7, color="purple", markerfacecolor="white",
                markeredgewidth=2)
        ax.fill_between(years, gdp_values, alpha=0.15, color="purple")

        # annotate first and last
        ax.annotate(f"${gdp_values[0]:,.1f}T",
                    (years[0], gdp_values[0]),
                    textcoords="offset points", xytext=(5, 10), fontsize=9)
        ax.annotate(f"${gdp_values[-1]:,.1f}T",
                    (years[-1], gdp_values[-1]),
                    textcoords="offset points", xytext=(-40, 10), fontsize=9)

        ax.set_title(f"Total Global GDP Trend ({start_year}–{end_year})",
                     fontsize=16, fontweight="bold", pad=15)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Total Global GDP (Trillions USD)", fontsize=12)
        ax.set_xticks(years)
        ax.set_xticklabels(years, rotation=45)
        ax.grid(True, alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fname = f"5_global_gdp_trend_{start_year}_{end_year}.png"
        self._save(plt, fname)

    # ── Chart 6: Fastest Growing Continent ───────────────────────────────
    def _chart_fastest_growing(self, data: Dict, start_year: int, end_year: int, plt) -> None:
        if not data:
            print("  Skipped fastest-growing (no data)")
            return

        continent   = data.get("continent", "Unknown")
        growth_rate = data.get("growth_rate", 0)
        start_gdp   = data.get("start_gdp", 0) / 1e12
        end_gdp     = data.get("end_gdp", 0) / 1e12

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # left: growth rate bar
        axes[0].bar([continent], [growth_rate], color="gold",
                    edgecolor="darkorange", linewidth=1.5, width=0.4)
        axes[0].text(0, growth_rate + growth_rate * 0.03,
                     f"{growth_rate:.1f}%", ha="center", fontsize=14, fontweight="bold")
        axes[0].set_title(f"Fastest Growing Continent\n({start_year}–{end_year})",
                          fontsize=14, fontweight="bold")
        axes[0].set_ylabel("Growth Rate (%)", fontsize=11)
        axes[0].grid(axis="y", alpha=0.3)
        axes[0].spines["top"].set_visible(False)
        axes[0].spines["right"].set_visible(False)

        # right: start vs end GDP comparison
        axes[1].bar([str(start_year), str(end_year)], [start_gdp, end_gdp],
                    color=["#3498db", "#2ecc71"], edgecolor="black", linewidth=0.7)
        axes[1].set_title(f"{continent}: GDP Comparison", fontsize=14, fontweight="bold")
        axes[1].set_ylabel("Total GDP (Trillions USD)", fontsize=11)
        for i, (label, val) in enumerate(zip([str(start_year), str(end_year)],
                                              [start_gdp, end_gdp])):
            axes[1].text(i, val + max(start_gdp, end_gdp) * 0.02,
                         f"${val:,.2f}T", ha="center", fontsize=11)
        axes[1].grid(axis="y", alpha=0.3)
        axes[1].spines["top"].set_visible(False)
        axes[1].spines["right"].set_visible(False)

        fname = f"6_fastest_growing_continent_{start_year}_{end_year}.png"
        self._save(plt, fname)

    # ── Chart 7: Declining Countries ─────────────────────────────────────
    def _chart_declining_countries(self, data, continent: str, plt) -> None:
        if not data:
            print(f"  No declining countries found in {continent} — skipping chart")
            # create an info chart
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.text(0.5, 0.5,
                    f"No countries in {continent}\nshowed consistent GDP decline.",
                    ha="center", va="center", fontsize=16, color="gray",
                    transform=ax.transAxes)
            ax.set_title(f"Countries with GDP Decline — {continent}",
                         fontsize=15, fontweight="bold")
            ax.axis("off")
            fname = f"7_declining_countries_{continent.replace(' ', '_')}.png"
            self._save(plt, fname)
            return

        countries      = [d["country"] for d in data]
        decline_pct    = [abs(d["decline_percent"]) for d in data]

        fig, ax = plt.subplots(figsize=(14, 7))
        bars = ax.barh(countries, decline_pct,
                       color="crimson", edgecolor="darkred", linewidth=0.7)

        for bar, val in zip(bars, decline_pct):
            ax.text(bar.get_width() + max(decline_pct) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}%", va="center", fontsize=9)

        ax.set_title(f"Countries with Consistent GDP Decline in {continent}",
                     fontsize=15, fontweight="bold", pad=15)
        ax.set_xlabel("Total Decline (%)", fontsize=12)
        ax.set_ylabel("Country", fontsize=12)
        ax.grid(axis="x", alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fname = f"7_declining_countries_{continent.replace(' ', '_')}.png"
        self._save(plt, fname)

    # ── Chart 8: Continental Contribution Pie ────────────────────────────
    def _chart_contribution_pie(self, data, start_year: int, end_year: int, plt) -> None:
        if not data:
            print("  Skipped contribution-pie (no data)")
            return

        continents    = [d["continent"] for d in data]
        contributions = [d["contribution_percent"] for d in data]

        # explode the largest slice slightly
        max_idx = contributions.index(max(contributions))
        explode = [0.05 if i == max_idx else 0 for i in range(len(continents))]

        colors = plt.cm.Set2.colors[: len(continents)]

        fig, ax = plt.subplots(figsize=(12, 9))
        wedges, texts, autotexts = ax.pie(
            contributions,
            labels=continents,
            autopct="%1.1f%%",
            startangle=140,
            explode=explode,
            colors=colors,
            pctdistance=0.82,
            labeldistance=1.05,
        )

        for autotext in autotexts:
            autotext.set_fontsize(9)
        for text in texts:
            text.set_fontsize(11)

        ax.set_title(
            f"Contribution of Each Continent to Global GDP\n({start_year}–{end_year})",
            fontsize=15, fontweight="bold", pad=20,
        )

        # legend with values
        legend_labels = [
            f"{c} — {p:.1f}%" for c, p in zip(continents, contributions)
        ]
        ax.legend(wedges, legend_labels,
                  title="Continents", loc="lower left",
                  bbox_to_anchor=(-0.1, -0.1), fontsize=9)

        fname = f"8_continent_contribution_{start_year}_{end_year}.png"
        self._save(plt, fname)