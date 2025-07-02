# Economic Recession Analysis

This ongoing project uses macroeconomic time series data to identify, analyze, predict, and visualize historical patterns around U.S. recessions. The goal is to explore key indicators that precede or coincide with recessionary periods and to provide a foundation for building predictive or diagnostic models.

## To Do

- [ ] Data Collection & Processing
- [ ] Analysis & Modeling
- [ ] Visualization & Reporting
- [ ] Documentation & Infrastructure

## Project Architecture

```
recession-indicator/
├── data/          	        	
│   ├── raw/                    	
│   │   ├── raw_fred.db         	# FRED data
│   │   └── raw_yahoo.db        	# yahoo finance data
│   └── processed/              	
│       └── processed_fred.db
├── notebooks/
│   └── eda/                    	# exploratory data analysis notebooks
│       └── fred.ipynb
├── src/                        	
│   ├── data_pipeline.py        	# ETL pipeline orchestration script
│   ├── extract_raw_data_fred.py
│   ├── extract_raw_data_yahoo.py
│   └── transform_raw_data_fred.py
├── config.json                 	
├── .gitignore
└── README.md
```

## Data

### Federal Reserve Economic Data | FRED

#### Production & Growth
- US Recession Indicator (USRECQ): quarterly indicator of recession periods as defined by the NBER; 1 indicates recession, 0 indicates expansion.
- Real GDP (GDPC1): Quarterly inflation-adjusted GDP in billions of dollars, indicating overall economic activity.
- Real GDP Growth (GDPC1_GROWTH): Quarterly percent change in Real GDP, reflecting economic expansion or contraction.
- Industrial Production (INDPRO): Monthly output of the industrial sector, an indicator of economic strength.
- Housing Starts (HOUST): Monthly number of new residential construction projects initiated; signals housing market health.

#### Yield Curve & Rates
- 10Y–3M Treasury Spread (T10Y3M): Difference between 10-year and 3-month Treasury yields; predictor of recessions.
- 10Y Treasury Yield (GS10): Benchmark yield indicating investor sentiment on long-term growth and inflation expectations.
- 3M T-Bill Rate (TB3MS): Short-term risk-free rate; reflects monetary policy stance.
- Fed Funds Rate (FEDFUNDS): Central bank policy rate; influences borrowing costs and economic activity.

#### Labor Market
- Unemployment Rate (UNRATE): Monthly percentage of labor force unemployed; key recession indicator.
- Nonfarm Payrolls (PAYEMS): Monthly total employment excluding agriculture; signals labor market strength.
- Initial Jobless Claims (ICSA): Monthly sum of new unemployment benefit claims; early labor market stress indicator.
- Avg Hourly Earnings (AHETPI): Monthly average hourly wage; tracks wage inflation and consumer purchasing power.

#### Inflation & Prices
- CPI YoY (CPIAUCSL): Consumer price inflation including all items; measures general price increases.
- Core CPI YoY (CPILFESL): CPI excluding volatile food and energy prices; indicates underlying inflation trends.
- Core PCE YoY (PCEPILFE): Personal Consumption Expenditure inflation excluding food and energy; preferred Fed inflation measure.

#### Sentiment & Spending
- UMich Consumer Sentiment (UMCSENT): Monthly consumer confidence survey; forecasts consumer spending trends.
- Retail Sales (Control) (RSAFS): Core retail sales excluding volatile categories; measures underlying consumer spending.

#### Credit & Risk-Premia
- High-Yield Effective Yield (BAMLH0A0HYM2EY): Yield on high-yield corporate bonds; indicator of credit market conditions and risk appetite.

#### Commodities (Cost Shock)
- WTI Crude Oil (DCOILWTICO): Daily crude oil price; reflects commodity cost pressures impacting inflation and production costs.

#### Market Stress
- CBOE VIX Index (VIXCLS): Volatility index measuring investor fear and uncertainty in equity markets.

#### Equity Market
- S&P 500 (SP500): Benchmark equity index reflecting market performance and investor sentiment.

## References

- [FRED - Federal Reserve Economic Data](https://fred.stlouisfed.org/)
- [Yahoo Finance - S&P 500 Index (GSPC)](https://finance.yahoo.com/quote/%5EGSPC)

