# transform_data.py

import pandas as pd
import sqlite3
import matplotlib.dates as mdates

def transform_fred_data(lookback_months=12, input_path='../data/raw/raw_fred.db', output_path='../data/processed/processed_fred.db'):
    """
    Transform raw FRED data and save to processed SQLite database.
    
    Args:
        lookback_months (int): Number of months to look back for data
        input_path (str): Path to input SQLite database
        output_path (str): Path to output processed SQLite database
    """
    # Compute date ranges
    end = pd.Timestamp.today()
    slice_start = end - pd.DateOffset(months=lookback_months)

    # Read raw data
    in_conn = sqlite3.connect(input_path)
    raw_df = pd.read_sql('SELECT date, series_id, value FROM raw_data', in_conn, parse_dates=['date'])
    in_conn.close()

    # Pivot raw into time series dictionary
    series_dict = {
        sid: (g.set_index('date')['value']
                .sort_index()
             )
        for sid, g in raw_df.groupby('series_id')
    }

    # Aggregate ICSA weekly → monthly sum
    if 'ICSA' in series_dict:
        series_dict['ICSA'] = series_dict['ICSA'].resample('M').sum()

    # Compute YoY inflation % for CPI series
    for sid in ['CPIAUCSL', 'CPILFESL', 'PCEPILFE']:
        ts = series_dict[sid]
        yoy = ts.pct_change(periods=12) * 100
        series_dict[sid] = yoy.dropna()

    # Slice all series to lookback window
    processed_records = []
    for sid, ts in series_dict.items():
        sliced = ts.loc[slice_start:end]
        recs = pd.DataFrame({
            'date': sliced.index,
            'series_id': sid,
            'value': sliced.values
        })
        processed_records.append(recs)

    processed_df = pd.concat(processed_records, ignore_index=True)

    # Write to new SQLite
    out_conn = sqlite3.connect(output_path)
    processed_df.to_sql('processed_data', out_conn, if_exists='replace', index=False)
    out_conn.close()

    print(f"Wrote {output_path} → table 'processed_data' with columns (date, series_id, value).")
    return processed_df

if __name__ == "__main__":
    transform_fred_data()
