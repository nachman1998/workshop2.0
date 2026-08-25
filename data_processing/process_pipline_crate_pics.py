'''
This script is a simple batch driver: it scans an input directory for CSV
files (each presumably holding one file's worth of network sessions, in
the format expected by `box_pics_array_crator_sparte.py`), and for every
CSV file found, it shells out to that other script to convert it into
per-session 2D histogram `.npy` files.
'''

import os
import numpy as np
import argparse
import re

def pics_per_conn(input_dir,bin,TPS,DELTA_T,output_dir):
    '''
    Batch-process every CSV file in `input_dir` by invoking the
    `box_pics_array_crator_sparte.py` script on each one, producing
    per-session histogram `.npy` files in `output_dir`.
    '''

    os.makedirs(output_dir, exist_ok=True)
    # Iterate over every entry in the input directory.
    for filename in os.listdir(input_dir):
        if not filename.endswith(".csv"):
            # Only process CSV files; skip anything else ( other data)
            continue
        # Use the CSV filename (without extension) as the basename
        basename= os.path.splitext(filename)[0]
        filepath_csv = os.path.join(input_dir, filename)
        try:
            os.system(f"python .\\box_pics_array_crator_sparte.py --input {filepath_csv} --bin {bin} --TPS {TPS} --DELTA_T {DELTA_T} --out_file {os.path.join(output_dir, basename+"_")}")
        except:
            print("failed pics_array_crator")
            continue



if __name__ == '__main__':
    parser = argparse.ArgumentParser( )
    parser.add_argument('--input_dir',      required=True,       help='Path to npys dir')    # Directory containing the input CSV files to batch-process.

    parser.add_argument("--bin", required=False,type=int,default=5)    # Bin width, forwarded to the underlying histogram-building script.

    parser.add_argument("--TPS", required=False,type=int,default=60)    # Sliding window length in seconds, forwarded as --TPS.

    parser.add_argument("--DELTA_T", required=False,type=int,default=60)    # Step size between windows in seconds, forwarded as --DELTA_T.

    parser.add_argument('--output_dir', required=True, )    # Directory where all generated .npy files will be written.

    args = parser.parse_args()
    pics_per_conn(
        args.input_dir,
        args.bin,
        args.TPS,
        args.DELTA_T,
        args.output_dir
    )