# GDP Analysis System — Phase 2

## Project Description

A modular GDP analysis system built on **Dependency Inversion Principle (DIP)**.  
Processes World Bank GDP data using functional programming and a clean plugin architecture.

## Team

| Member | Responsibility |
|--------|---------------|
| **Amna Dilshad** | Architecture, `main.py`, `config.json`, `core/contracts.py`, `plugins/inputs.py` |
| **Fiza** | `core/engine.py` (9 analysis functions), `plugins/outputs.py` (8 charts), `__init__.py` files, README |

---

## Project Structure

```
SDA_GDP_Phase2/
├── main.py                  ← Orchestrator (Amna)
├── config.json              ← Configuration (switch inputs/outputs/params)
├── testing.py               ← Tests (Amna)
├── core/
│   ├── __init__.py          ← Fiza
│   ├── contracts.py         ← Protocols / interfaces (Amna)
│   └── engine.py            ← All 9 analysis functions (Fiza)
├── plugins/
│   ├── __init__.py          ← Fiza
│   ├── inputs.py            ← JSONReader, CSVReader (Amna)
│   └── outputs.py           ← ConsoleWriter, GraphicsChartWriter (Fiza)
└── data/
    ├── gdp_with_continent_filled.json
    └── gdp_with_continent_filled.xlsx
```

---

## Architecture — Dependency Inversion Principle

```
┌─────────────────────────────────────────────────────┐
│  main.py  (Orchestrator)                            │
│  reads config.json → wires components together      │
└─────────────┬────────────────────┬──────────────────┘
              │ injects            │ injects
              ▼                    ▼
 ┌────────────────────┐   ┌──────────────────────┐
 │  plugins/inputs.py │   │ plugins/outputs.py   │
 │  JSONReader        │   │ ConsoleWriter        │
 │  CSVReader         │   │ GraphicsChartWriter  │
 └────────┬───────────┘   └──────────┬───────────┘
          │ calls PipelineService    │ implements DataSink
          ▼                          ▼
 ┌────────────────────────────────────────────────┐
 │         core/engine.py                        │
 │  TransformationEngine                         │
 │  – owns contracts (DataSink, PipelineService) │
 │  – 9 analysis functions                       │
 │  – NEVER imports a specific reader/writer     │
 └────────────────────────────────────────────────┘
```

**Core owns the contracts. Plugins depend on Core. Core never depends on plugins.**

---

## How to Run

### 1. Install dependencies
```bash
pip install pandas matplotlib seaborn openpyxl
```

### 2. Configure `config.json`
```json
{
  "data_source": {
    "type": "json",
    "filepath": "data/gdp_with_continent_filled.json"
  },
  "output": {
    "type": "graphics",
    "output_dir": "output"
  },
  "analysis": {
    "continent": "Asia",
    "year": 2020,
    "start_year": 2015,
    "end_year": 2020,
    "decline_years": 3
  }
}
```

### 3. Run
```bash
python main.py
```

Charts are saved to `output/` folder.

---

## Config-Driven Design ⚠️

**Every chart title, filename, and filter uses values from `config.json`.**

To verify:
1. Change `"continent": "Europe"` and `"year": 2019`
2. Run again → all charts should say "Europe" and "2019"
3. If they still say "Asia" or "2020" → hardcoded = FAIL ❌

---

## Analyses Performed

| # | Analysis | Output |
|---|----------|--------|
| 1 | Top 10 Countries by GDP | Horizontal bar chart |
| 2 | Bottom 10 Countries by GDP | Horizontal bar chart |
| 3 | GDP Growth Rate per Country | Vertical bar chart (green/red) |
| 4 | Average GDP by Continent | Bar chart |
| 5 | Total Global GDP Trend | Line chart with fill |
| 6 | Fastest Growing Continent | Dual-panel bar chart |
| 7 | Countries with Consistent GDP Decline | Horizontal bar chart |
| 8 | Continental Contribution to Global GDP | Pie chart with legend |

---

## Testing
```bash
python testing.py
```

---

## Key Libraries
- `pandas` — data manipulation
- `matplotlib` — chart generation
- `typing.Protocol` — structural interfaces (DIP)

---

## Date
March 2025 | Software Design and Analysis — Phase 2
