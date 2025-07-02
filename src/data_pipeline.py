# data_pipeline.py

import os
import sys
from pathlib import Path
import pandas as pd
from extract_raw_data_fred import extract_fred_data
from extract_raw_data_yahoo import extract_yahoo_data
from transform_raw_data_fred import transform_fred_data

def run_fred_pipeline(lookback_months=12, 
                     config_path='../config.json',
                     raw_data_path='../data/raw/raw_fred.db',
                     processed_data_path='../data/processed/processed_fred.db',
                     skip_extract=False):
    """
    Run the complete FRED data pipeline: extract → transform.
    
    Args:
        lookback_months (int): Number of months to look back for data
        config_path (str): Path to config.json file containing FRED API key
        raw_data_path (str): Path to raw data SQLite database
        processed_data_path (str): Path to processed data SQLite database
        skip_extract (bool): Skip the extract step if raw data already exists
    """
    print("=" * 25)
    print("   FRED Data Pipeline")
    print("=" * 25)
    
    # Calculate time period
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.DateOffset(months=lookback_months)
    print(f"Period: {start_date.strftime('%Y-%m')} to {end_date.strftime('%Y-%m')}")
    
    # Ensure data directories exist
    raw_dir = Path(raw_data_path).parent
    processed_dir = Path(processed_data_path).parent
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Extract raw data
    if not skip_extract:
        print("\nStep 1: Extracting data...")
        try:
            raw_df = extract_fred_data(
                lookback_months=lookback_months,
                config_path=config_path,
                output_path=raw_data_path
            )
            print(f"  Extracted {len(raw_df)} records")
        except Exception as e:
            print(f"  Extraction failed: {e}")
            return False
    else:
        print("\nStep 1: Skipping extraction")
    
    # Step 2: Transform raw data
    print("\nStep 2: Transforming data...")
    try:
        processed_df = transform_fred_data(
            lookback_months=lookback_months,
            input_path=raw_data_path,
            output_path=processed_data_path
        )
        print(f"  Processed {len(processed_df)} records")
    except Exception as e:
        print(f"  Transformation failed: {e}")
        return False
    
    print("\n" + "=" * 25)
    print("   Pipeline Complete")
    print("=" * 25)
    return True

def run_yahoo_pipeline(ticker="^GSPC",
                      start_date="1969-01-01", 
                      end_date=None,
                      raw_data_path='../data/raw/raw_yahoo.db',
                      skip_extract=False):
    """
    Run the Yahoo Finance data pipeline: extract raw data.
    
    Args:
        ticker (str): Yahoo Finance ticker symbol (default: ^GSPC for S&P 500)
        start_date (str): Start date for data extraction (default: "1969-01-01")
        end_date (str): End date for data extraction (default: today)
        raw_data_path (str): Path to raw data SQLite database
        skip_extract (bool): Skip the extract step if raw data already exists
    """
    print("=" * 27)
    print("   Yahoo Finance Pipeline")
    print("=" * 27)
    
    # Display time period
    if end_date is None:
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    print(f"Ticker: {ticker}")
    print(f"Period: {start_date} to {end_date}")
    
    # Ensure data directories exist
    raw_dir = Path(raw_data_path).parent
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Extract raw data
    if not skip_extract:
        print("\nStep 1: Extracting data...")
        try:
            raw_df = extract_yahoo_data(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                output_path=raw_data_path
            )
            print(f"  Extracted {len(raw_df)} records")
        except Exception as e:
            print(f"  Extraction failed: {e}")
            return False
    else:
        print("\nStep 1: Skipping extraction")
    
    print("\n" + "=" * 27)
    print("   Pipeline Complete")
    print("=" * 27)
    return True

def main():
    """Main function to run the pipeline with command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Data Pipeline for FRED and Yahoo Finance')
    parser.add_argument('--pipeline', choices=['fred', 'yahoo', 'both'], default='both',
                       help='Which pipeline to run (default: both)')
    
    # FRED-specific arguments
    parser.add_argument('--lookback', type=int, default=12,
                       help='Number of months to look back for FRED data (default: 12)')
    parser.add_argument('--config', type=str, default='../config.json',
                       help='Path to config.json file (default: ../config.json)')
    parser.add_argument('--fred-raw-path', type=str, default='../data/raw/raw_fred.db',
                       help='Path to FRED raw data database (default: ../data/raw/raw_fred.db)')
    parser.add_argument('--processed-path', type=str, default='../data/processed/processed_fred.db',
                       help='Path to processed data database (default: ../data/processed/processed_fred.db)')
    
    # Yahoo-specific arguments
    parser.add_argument('--ticker', type=str, default='^GSPC',
                       help='Yahoo Finance ticker symbol (default: ^GSPC)')
    parser.add_argument('--start-date', type=str, default='1969-01-01',
                       help='Start date for Yahoo data (default: 1969-01-01)')
    parser.add_argument('--end-date', type=str, default=None,
                       help='End date for Yahoo data (default: today)')
    parser.add_argument('--yahoo-raw-path', type=str, default='../data/raw/raw_yahoo.db',
                       help='Path to Yahoo raw data database (default: ../data/raw/raw_yahoo.db)')
    
    # Common arguments
    parser.add_argument('--skip-extract', action='store_true',
                       help='Skip extraction step if raw data already exists')
    
    args = parser.parse_args()
    
    success = True
    
    # Run FRED pipeline
    if args.pipeline in ['fred', 'both']:
        fred_success = run_fred_pipeline(
            lookback_months=args.lookback,
            config_path=args.config,
            raw_data_path=args.fred_raw_path,
            processed_data_path=args.processed_path,
            skip_extract=args.skip_extract
        )
        success = success and fred_success
    
    # Run Yahoo pipeline
    if args.pipeline in ['yahoo', 'both']:
        yahoo_success = run_yahoo_pipeline(
            ticker=args.ticker,
            start_date=args.start_date,
            end_date=args.end_date,
            raw_data_path=args.yahoo_raw_path,
            skip_extract=args.skip_extract
        )
        success = success and yahoo_success
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 