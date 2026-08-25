"""
This script combines many small per-session `.npy` files
into one or two large `.npy` dataset files, ready to
be fed into the anomaly-detection pipeline.

 (`unify_npy`): Plain unification load every `.npy` file in the input
 directory and concatenate them all (along axis 0) into a single
 output `.npy` file. This is the default mode.
"""

import os
import random
import numpy as np
import argparse
import re

def unify_npy(dir_path,output_dir,out_file):
    os.makedirs(output_dir, exist_ok=True)
    concat_list = []
    # Load every .npy file in the directory into a list of arrays.
    for filename in os.listdir(dir_path):
        path = os.path.join(dir_path, filename)

        if os.path.isfile(path) and filename.endswith(".npy"):
            print(path)
            concat_list.append(np.load(path))# Stack all loaded arrays together along the first axis
    dataset = np.concatenate(concat_list,axis=0)
    np.save(os.path.join(output_dir,out_file), dataset)    # Save the combined dataset as a single .npy file.

#this function is not used
def unify_npy_split(dir_path,p,output_dir,out_file):
    os.makedirs(output_dir, exist_ok=True)
    pr=p/100
    concat_list_train = []
    concat_list_test = []
    for filename in os.listdir(dir_path):
        path = os.path.join(dir_path, filename)

        if os.path.isfile(path) and filename.endswith(".npy"):
            print(path)
            array = np.load(path)
            np.random.shuffle(array)

            split_idx = int(len(array) * (1 - pr))

            concat_list_train.extend(array[:split_idx])
            concat_list_test.extend(array[split_idx:])
    print(len(concat_list_train), len(concat_list_test))
    actual_split=len(concat_list_test)/(len(concat_list_train)+len(concat_list_test))
    if actual_split <pr-0.05 or actual_split> pr+0.05:
        if actual_split < pr - 0.05:
            need_to_take=pr-actual_split
            total = len(concat_list_train) + len(concat_list_test)
            n_to_move = round(need_to_take * total)

            random.shuffle(concat_list_train)
            concat_list_test.extend(concat_list_train[:n_to_move])
            concat_list_train = concat_list_train[n_to_move:]
        else:
            need_to_take = -pr + actual_split
            total = len(concat_list_train) + len(concat_list_test)
            print(total)
            n_to_move = round(need_to_take * total)
            random.shuffle(concat_list_test)
            concat_list_train.extend(concat_list_test[:n_to_move])
            concat_list_test = concat_list_test[n_to_move:]

    dataset_train = np.array(concat_list_train)
    dataset_test = np.array(concat_list_test)
    np.save(os.path.join(output_dir,out_file)+"_train", dataset_train)
    np.save(os.path.join(output_dir,out_file) + "_test", dataset_test)





if __name__ == '__main__':
    parser = argparse.ArgumentParser( )
    parser.add_argument('--input_dir',      required=True, help='Path to npys dir')    # Directory containing the individual .npy files to combine.

    parser.add_argument('--split', action='store_true', default=False) #not in use
    parser.add_argument("--percent",  type=int, default=20, help="split percent") #not in use
    parser.add_argument('--output_dir', required=True)    # Directory to write the output file(s) into.

    parser.add_argument('--out_file_name', required=True)    # Base output filename (extension/suffixes are added automatically).

    args = parser.parse_args()
    if args.split:
        unify_npy_split(
            args.input_dir,
            args.percent,
            args.output_dir,
            args.out_file_name
        )
    else:
        unify_npy(args.input_dir,args.output_dir,args.out_file_name)