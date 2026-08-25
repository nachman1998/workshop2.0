"""
This is the top-level orchestrator script that runs the full data
pipeline end-to-end, in sequence, by shelling out to each of the other
scripts in the project:


  1. (for first run) `generic_parser.py`
  converting raw captures into the per-connection CSV format expected by later steps

  2. `process_pipline_filter_csv_with_HAR.py`
     For each CSV with a matching HAR
       file in `input_dir`, filters it down to only the connections seen
       in the HAR capture, writing results into `<input_dir>\\filterd_csv`.

  3. `process_pipline_crate_pics.py`
     Converts each filtered CSV in
       `<input_dir>\\filterd_csv` into per-session 2D histogram `.npy` files,
       written into `<input_dir>\\_pics`.

  4. `process_pipline_unify.py`
       Combines all the per-session `.npy` files from `<input_dir>\\_pics`
       into one  combined dataset
       file(s) under `<input_dir>\\_unified_pics`, named using
       `out_file_name`.

"""

import os
import random
import numpy as np
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser( )
    # Root directory containing the raw input data; also used as the base
    # path for all intermediate/output subdirectories created by each
    # pipeline stage (filterd_csv, _pics, _unified_pics).
    parser.add_argument('--input_dir',      required=True, help='Path to npys dir')
    # If set, run the optional generic parsing stage before filtering.
    parser.add_argument('--parse', action='store_true', default=False)
    parser.add_argument('--split', action='store_true', default=False)#not in use
    # Histogram bin width, forwarded to the picture-creation stage.
    parser.add_argument("--bin", required=False,type=int,default=7)#but using default
    # Sliding window length in seconds
    parser.add_argument("--TPS", required=False,type=int,default=60)
    # Step size between windows in seconds
    parser.add_argument("--DELTA_T", required=False,type=int,default=60)
    parser.add_argument("--percent",  type=int, default=20, help="split percent")#not in use
    # Base name for the final combined output dataset
    parser.add_argument('--out_file_name', required=True)
    args = parser.parse_args()

    if args.parse:
        os.system(f"python .\\generic_parser.py --input {args.input_dir}")

    os.system(f"python .\\process_pipline_filter_csv_with_HAR.py --input_dir {args.input_dir} --output_dir {args.input_dir+"\\filterd_csv"} ")

    os.system(f"python .\\process_pipline_crate_pics.py --input_dir {args.input_dir+"\\filterd_csv"} --bin {args.bin} --TPS {args.TPS} --DELTA_T {args.DELTA_T} --output_dir {args.input_dir+"\\_pics"} ")


    if args.split:
        os.system(f"python .\\process_pipline_unify.py --input_dir {args.input_dir+"\\_pics"} --output_dir {args.input_dir+"\\_unified_pics"} --out_file_name {args.out_file_name} --split --percent {args.percent} ")
    else:
        os.system(f"python .\\process_pipline_unify.py --input_dir {args.input_dir+"\\_pics"} --output_dir {args.input_dir+"\\_unified_pics"} --out_file_name {args.out_file_name}")
