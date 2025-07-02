# Economic Recession Analysis

## Architecture

```
RECESSION-INDICATOR/
├── data/                       # All dataset files
│   ├── raw/                    # Unprocessed source data
│   │   ├── raw_fred.db         # FRED data
│   │   └── raw_yahoo.db        # Yahoo Finance data
│   └── processed/              # Transformed/cleaned data
│       └── processed_fred.db
├── notebooks/
│   └── eda/                    # Exploratory data analysis notebooks
│       └── fred.ipynb
├── src/                        # Source scripts for ETL pipeline
│   ├── data_pipeline.py        # Orchestration script
│   ├── extract_raw_data_fred.py
│   ├── extract_raw_data_yahoo.py
│   └── transform_raw_data_fred.py
├── config.json                 # API keys or configuration settings
├── .gitignore
└── README.md
```

## Data

### Federal Reserve Economic Data | FRED

#### Production & Growth
- Real GDP: Quarterly inflation-adjusted GDP in billions of dollars, indicating overall economic activity.
- Real GDP Growth: Quarterly percent change in Real GDP, reflecting economic expansion or contraction.
- Industrial Production: Monthly output of the industrial sector, an indicator of economic strength.
- Housing Starts: Monthly number of new residential construction projects initiated; signals housing market health.

#### Yield Curve & Rates
- 10Y–3M Treasury Spread: Difference between 10-year and 3-month Treasury yields; predictor of recessions.
- 10Y Treasury Yield: Benchmark yield indicating investor sentiment on long-term growth and inflation expectations.
- 3M T-Bill Rate: Short-term risk-free rate; reflects monetary policy stance.
- Fed Funds Rate: Central bank policy rate; influences borrowing costs and economic activity.

#### Labor Market
- Unemployment Rate: Monthly percentage of labor force unemployed; key recession indicator.
- Nonfarm Payrolls: Monthly total employment excluding agriculture; signals labor market strength.
- Initial Jobless Claims: Monthly sum of new unemployment benefit claims; early labor market stress indicator.
- Avg Hourly Earnings: Monthly average hourly wage; tracks wage inflation and consumer purchasing power.

#### Inflation & Prices
- CPI YoY: Consumer price inflation including all items; measures general price increases.
- Core CPI YoY: CPI excluding volatile food and energy prices; indicates underlying inflation trends.
- Core PCE YoY: Personal Consumption Expenditure inflation excluding food and energy; preferred Fed inflation measure.

#### Sentiment & Spending
- UMich Consumer Sentiment: Monthly consumer confidence survey; forecasts consumer spending trends.
- Retail Sales (Control): Core retail sales excluding volatile categories; measures underlying consumer spending.

#### Credit & Risk-Premia
- High-Yield Effective Yield: Yield on high-yield corporate bonds; indicator of credit market conditions and risk appetite.

#### Commodities (Cost Shock)
- WTI Crude Oil: Daily crude oil price; reflects commodity cost pressures impacting inflation and production costs.

#### Market Stress
- CBOE VIX Index: Volatility index measuring investor fear and uncertainty in equity markets.

#### Equity Market
- S&P 500: Benchmark equity index reflecting market performance and investor sentiment.

## References

- [FRED - Federal Reserve Economic Data](https://fred.stlouisfed.org/)

