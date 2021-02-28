#!/usr/bin/python3

import argparse
import os
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

def compare_files(filename, filepath_one, filepath_two, print_type):
    file_one = read_file_as_bytearray(filepath_one)
    file_two = read_file_as_bytearray(filepath_two)
    are_equal = get_str_hash(file_one) == get_str_hash(file_two)
    if are_equal and print_type in ("all", "equals"):
        print(f"{filename} OK")
    if not are_equal and print_type in ("all", "diffs"):
        print(f"{filename} not OK")
        len_one = len(file_one)
        len_two = len(file_two)
        if len_one != len_two:
            div = 0
            if len_two != 0:
                div = round(len_one/len_two, 3)
            print(f"\tSize doesn't match: {len_one} vs {len_two} (x{div}) ({len_one-len_two})")
        else:
            print("\tSize matches.")
    return are_equal


def compare_baseroms(second_baserom_path, print_type):
    files_baserom_one = set()
    files_baserom_two = set()

    missing_in_two = set()
    missing_in_one = set()

    equals = 0
    different = 0

    for filename in os.listdir(baserom_path):
        files_baserom_one.add(filename)
        filepath_one = os.path.join(baserom_path, filename)
        filepath_two = os.path.join(second_baserom_path, filename)
        if not os.path.exists(filepath_two):
            missing_in_two.add(filename)
            if print_type in ("all", "missing"):
                print(f"File {filename} in baserom does not exists in other_baserom")
            continue
        
        if not compare_files(filename, filepath_one, filepath_two, print_type):
            different += 1
        else:
            equals += 1
    
    for filename in os.listdir(second_baserom_path):
        files_baserom_two.add(filename)
        if filename not in files_baserom_one:
            missing_in_one.add(filename)
            if print_type in ("all", "missing"):
                print(f"File {filename} from other_baserom does not exists in baserom")

    total = len(files_baserom_one)
    if total > 0:
        print()
        if print_type in ("all", "equals"):
            print(f"Equals:     {equals}/{total} ({round(100*equals/total, 2)}%)")
        if print_type in ("all", "diffs"):
            print(f"Differents: {different}/{total} ({round(100*different/total, 2)}%)")
        if print_type in ("all", "missing"):
            missing = len(missing_in_two)
            print(f"Missing:    {missing}/{total} ({round(100*missing/total, 2)}%)")
            print(f"Extras:     {len(missing_in_one)}")


def main():
    description = ""

    epilog = """\
    """
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("other_baserom", help="Path to the baserom folder that will be compared against.")
    parser.add_argument("--print", help="Select what will be printed for a cleaner output. Default is 'all'.", choices=["all", "equals", "diffs", "missing"], default="all")
    args = parser.parse_args()

    compare_baseroms(args.other_baserom, args.print)


if __name__ == "__main__":
    main()
