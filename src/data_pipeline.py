# data_pipeline.py

import os
import sys
from pathlib import Path
import pandas as pd
from extract_raw_data_fred import extract_fred_data
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

def main():
    """Main function to run the pipeline with command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description='FRED Data Pipeline')
    parser.add_argument('--lookback', type=int, default=12,
                       help='Number of months to look back (default: 12)')
    parser.add_argument('--config', type=str, default='../config.json',
                       help='Path to config.json file (default: ../config.json)')
    parser.add_argument('--raw-path', type=str, default='../data/raw/raw_fred.db',
                       help='Path to raw data database (default: ../data/raw/raw_fred.db)')
    parser.add_argument('--processed-path', type=str, default='../data/processed/processed_fred.db',
                       help='Path to processed data database (default: ../data/processed/processed_fred.db)')
    parser.add_argument('--skip-extract', action='store_true',
                       help='Skip extraction step if raw data already exists')
    
    args = parser.parse_args()
    
    success = run_fred_pipeline(
        lookback_months=args.lookback,
        config_path=args.config,
        raw_data_path=args.raw_path,
        processed_data_path=args.processed_path,
        skip_extract=args.skip_extract
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 