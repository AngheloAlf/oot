#!/usr/bin/python3

import argparse
import os
import sys
import struct
import hashlib

script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = script_dir + "/.."
if not script_dir.endswith("/tools"):
    root_dir = script_dir
baserom_path = root_dir + "/baserom"


def get_str_hash(byte_array):
    return str(hashlib.md5(byte_array).hexdigest())

def read_file_as_bytearray(filepath):
    with open(filepath, mode="rb") as f:
        return bytearray(f.read())

def compare_files(filename, filepath_one, filepath_two):
    file_one = read_file_as_bytearray(filepath_one)
    file_two = read_file_as_bytearray(filepath_two)
    are_equal = get_str_hash(file_one) == get_str_hash(file_two)
    if are_equal:
        print(f"{filename} OK")
    if not are_equal:
        print(f"{filename} not OK")
        len_one = len(file_one)
        len_two = len(file_two)
        if len_one != len_two:
            div = 0
            if len_two != 0:
                div = round(len_one/len_two, 3)
            print(f"\tSize don't match: {len_one} vs {len_two} (x{div})")
        else:
            print("\tSize matches.")
    return are_equal


def compare_baseroms(second_baserom_path):
    total = 0
    equals = 0
    missing = 0
    different = 0
    for filename in os.listdir(baserom_path):
        total += 1
        filepath_one = os.path.join(baserom_path, filename)
        filepath_two = os.path.join(second_baserom_path, filename)
        if not os.path.exists(filepath_two):
            missing += 1
            print(f"File {filename} does not exists in {second_baserom_path}")
            continue
        
        if not compare_files(filename, filepath_one, filepath_two):
            different += 1
        else:
            equals += 1
    
    if total > 0:
        print()
        print(f"Equals:     {equals}/{total} ({round(100*equals/total, 2)}%)")
        print(f"Differents: {different}/{total} ({round(100*different/total, 2)}%)")
        print(f"Mising:     {missing}/{total} ({round(100*missing/total, 2)}%)")


def main():
    description = ""

    epilog = """\
    """
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("second_baserom", help="Path to the baserom folder that will be compared against.")
    args = parser.parse_args()

    compare_baseroms(args.second_baserom)


if __name__ == "__main__":
    main()
