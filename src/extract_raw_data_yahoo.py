import yfinance as yf
import pandas as pd
import sqlite3

def extract_yahoo_data(ticker="^GSPC", start_date="1969-01-01", end_date=None, output_path='../data/raw/raw_yahoo.db'):
    """
    Extract Yahoo Finance data and save to SQLite database.
    
    Args:
        ticker (str): Yahoo Finance ticker symbol (default: ^GSPC for S&P 500)
        start_date (str): Start date for data extraction (default: "1969-01-01")
        end_date (str): End date for data extraction (default: today)
        output_path (str): Path to output SQLite database
    """
    # Set end date to today if not provided
    if end_date is None:
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    
    # Fetch data from Yahoo Finance
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    
    # Reset index to make date a column
    df = df.reset_index()
    df.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)
    
    # Write to SQLite - keep all original columns
    conn = sqlite3.connect(output_path)
    df.to_sql('sp500', conn, if_exists='replace', index=False)
    conn.close()

    print(f"Wrote {output_path} → table 'sp500' with {len(df.columns)} columns and {len(df)} rows.")
    print(f"Columns: {list(df.columns)}")
    print(f"Extracted data for ticker {ticker}")
    return df

if __name__ == "__main__":
    extract_yahoo_data()


