'''
This script is  batch driver for a filtering step. For each session CSV file in `input_dir`
that has a matching
`.har` (HTTP Archive) file with the same basename, it:

  1. Runs `HAR_filter.py` on the `.har` file to produce a temporary
     "filter" CSV
  2. Runs `filter_conn_csv_with_filter_csv.py` to filter the original
     session CSV down to only the rows that match entries in that
     temporary filter CSV, writing the result into `output_dir`.
  3. Deletes the temporary filter CSV.

Files whose basename contains "temp" are skipped (to avoid reprocessing
leftover temporary files from a previous/interrupted run), and CSV files
without a matching `.har` file are skipped entirely, since there's nothing
to filter against.
'''

import os
import numpy as np
import argparse
import re

def filter_per_conn_for_dir(input_dir,output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        # Only consider CSV files as the starting point (we look for a
        # matching .har file for each one below).
        if not filename.endswith(".csv"):
            continue
        basename = os.path.splitext(filename)[0]
        if "temp" in basename:
            continue
        print(basename)
        filepath_csv = os.path.join(input_dir, basename + '.csv')
        filepath_har = os.path.join(input_dir, basename+'.har')
        if not os.path.exists(filepath_har):
            continue
        print(filepath_har)
        # Path for a temporary intermediate CSV that HAR_filter.py will
        # produce from the HAR file -- this acts as the "filter list" of
        # connections to keep.
        tempout=os.path.join(input_dir, basename+'_temp.csv')
        try:
            os.system(f"python .\\HAR_filter.py --input {filepath_har} --out_name {tempout}")

        except:
            print("failed_har_filter")
            continue
        # Final output path for this file's filtered CSV.
        output_file = os.path.join(output_dir, "filterd_"+basename+".csv")

        # Filter the original session CSV, keeping only rows
        # whose connections also appear in the HAR-derived filter CSV
        try:
            os.system(f"python .\\filter_conn_csv_with_filter_csv.py --input {filepath_csv} --filter_csv {tempout} --out_file {output_file}")
        except:
            print("failed_to_filter_final_csv")

        if os.path.exists(tempout):
            os.remove(tempout)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='unify npys in dir.'
    )
    parser.add_argument('--input_dir',      required=True,       help='Path to npys dir')    # Directory containing the paired .csv/.har files to process.

    parser.add_argument('--output_dir', required=True, )    # Directory where the final filtered CSV files will be written.

    args = parser.parse_args()
    filter_per_conn_for_dir(
        args.input_dir,
        args.output_dir
    )