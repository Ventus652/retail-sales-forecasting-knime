# Data guide

The original course files are not redistributed in this public portfolio repository because they did not include an explicit reuse license.

## Expected files

### Store master data (`filialen.csv`)

| Column | Meaning |
|---|---|
| `Store` | Store identifier |
| `StoreType` | Store format category |
| `Assortment` | Assortment category |
| `CompetitionDistance` | Distance to nearest competitor |
| `CompetitionOpenSinceMonth` | Competitor opening month |
| `CompetitionOpenSinceYear` | Competitor opening year |
| `Promo2` | Participation in continuing promotion program |
| `Promo2SinceWeek` | Program start week |
| `Promo2SinceYear` | Program start year |
| `PromoInterval` | Months in which the promotion restarts |

### Daily sales data (`filialumsatz.csv`)

| Column | Meaning |
|---|---|
| `Store` | Store identifier |
| `DayOfWeek` | Weekday number |
| `Date` | Observation date |
| `Sales` | Daily sales target |
| `Customers` | Daily customer count |
| `Open` | Store-open indicator |
| `Promo` | Daily promotion indicator |
| `StateHoliday` | State-holiday category |
| `SchoolHoliday` | School-holiday indicator |

## Local layout

For local work, use the following folders; CSV files in them are ignored by Git:

```text
data/
├── raw/
│   ├── filialen.csv
│   └── filialumsatz.csv
└── processed/
    └── clean_retail_sales.csv
```

The original KNIME workflows contain machine-specific absolute paths. After importing a workflow, point its first CSV Reader node to the corresponding local file. If the data-quality workflow writes an output file, configure its CSV Writer to `data/processed/clean_retail_sales.csv`.
