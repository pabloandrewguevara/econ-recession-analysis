# extract_raw.py

import pandas as pd
import json
import sqlite3
from fredapi import Fred

def extract_fred_data(lookback_months=12, config_path='../config.json', output_path='../data/raw/raw_fred.db'):
    """
    Extract FRED data and save to SQLite database.
    
    Args:
        lookback_months (int): Number of months to look back for data
        config_path (str): Path to config.json file containing FRED API key
        output_path (str): Path to output SQLite database
    """
    # Load API key
    with open(config_path, 'r') as f:
        fred_api_key = json.load(f)['fred_api_key']
    fred = Fred(api_key=fred_api_key)

    # Compute date ranges
    end = pd.Timestamp.today()
    raw_start = end - pd.DateOffset(months=lookback_months + 12)

    # All series you need
    series_ids = [
        'T10Y3M','GS10','TB3MS','FEDFUNDS',  # Yield Curve & Rates
        'UNRATE','PAYEMS','ICSA','AHETPI',   # Labor Market
        'CPIAUCSL','CPILFESL','PCEPILFE',    # Inflation & Prices
        'GDPC1','INDPRO','HOUST',            # Production & Growth
        'BAMLH0A0HYM2EY','TEDRATE',          # Credit & Risk-Premia
        'UMCSENT','RSAFS',                   # Sentiment & Spending
        'VIXCLS',                            # Market Stress
        'DCOILWTICO',                        # Commodities
        'SP500'                              # Equity Market
    ]

    # Fetch each series into a single DataFrame
    frames = []
    for sid in series_ids:
        s = fred.get_series(sid, observation_start=raw_start, observation_end=end)
        df = s.to_frame(name='value')
        df['series_id'] = sid
        df.index.name = 'date'
        frames.append(df.reset_index())

    raw_df = pd.concat(frames, ignore_index=True)

    # Write to SQLite
    conn = sqlite3.connect(output_path)
    raw_df.to_sql('raw_data', conn, if_exists='replace', index=False)
    conn.close()

    print(f"Wrote {output_path} → table 'raw_data' with columns (date, series_id, value).")
    return raw_df

if __name__ == "__main__":
    extract_fred_data()

