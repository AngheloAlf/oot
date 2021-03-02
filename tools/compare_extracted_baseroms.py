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

def readFile(filepath):
    with open(filepath) as f:
        return [x.strip() for x in f.readlines()]

def read_file_as_bytearray(filepath):
    with open(filepath, mode="rb") as f:
        return bytearray(f.read())

def compare_files(filepath_one, filepath_two):
    file_one = read_file_as_bytearray(filepath_one)
    file_two = read_file_as_bytearray(filepath_two)
    are_equal = get_str_hash(file_one) == get_str_hash(file_two)
    len_one = len(file_one)
    len_two = len(file_two)
    return are_equal, len_one, len_two


def compare_baseroms(second_baserom_path, filelist, print_type):
    files_baserom_one = set()
    files_baserom_two = set()

    missing_in_one = set()
    missing_in_two = set()

    equals = 0
    different = 0

    for filename in filelist:
        filepath_one = os.path.join(baserom_path, filename)
        filepath_two = os.path.join(second_baserom_path, filename)

        is_missing = False

        if os.path.exists(filepath_one):
            files_baserom_one.add(filename)
        else:
            missing_in_one.add(filename)
            is_missing = True
            if print_type in ("all", "missing"):
                print(f"File {filename} does not exists in baserom.")

        if os.path.exists(filepath_two):
            files_baserom_two.add(filename)
        else:
            missing_in_two.add(filename)
            is_missing = True
            if print_type in ("all", "missing"):
                print(f"File {filename} does not exists in other_baserom.")

        if is_missing:
            continue

        are_equal, len_one, len_two = compare_files(filepath_one, filepath_two)
        if are_equal:
            equals += 1
            if print_type in ("all", "equals"):
                print(f"{filename} OK")
        else:
            different += 1
            if print_type in ("all", "diffs"):
                print(f"{filename} not OK")
                if len_one != len_two:
                    div = 0
                    if len_two != 0:
                        div = round(len_one/len_two, 3)
                    print(f"\tSize doesn't match: {len_one} vs {len_two} (x{div}) ({len_one-len_two})")
                else:
                    print("\tSize matches.")

    total = len(filelist)
    if total > 0:
        print()
        if print_type in ("all", "equals"):
            print(f"Equals:     {equals}/{total} ({round(100*equals/total, 2)}%)")
        if print_type in ("all", "diffs"):
            print(f"Differents: {different}/{total} ({round(100*different/total, 2)}%)")
        if print_type in ("all", "missing"):
            missing = len(missing_in_one)
            print(f"Missing:    {missing}/{total} ({round(100*missing/total, 2)}%)")
            print(f"Missing 2:  {len(missing_in_two)}")


def compare_to_csv(second_baserom_path, filelist, print_type):
    files_baserom_one = set()
    files_baserom_two = set()

    missing_in_one = set()
    missing_in_two = set()

    print("File,Are equals,Size in baserom,Size in other_baserom,Size proportion,Size difference")

    for filename in filelist:
        filepath_one = os.path.join(baserom_path, filename)
        filepath_two = os.path.join(second_baserom_path, filename)
        is_missing_in_one = False
        is_missing_in_two = False

        if os.path.exists(filepath_one):
            files_baserom_one.add(filename)
        else:
            missing_in_one.add(filename)
            is_missing_in_one = True

        if os.path.exists(filepath_two):
            files_baserom_two.add(filename)
        else:
            missing_in_two.add(filename)
            is_missing_in_two = True

        if is_missing_in_one or is_missing_in_two:
            if print_type in ("all", "missing"):
                len_one = ""
                len_two = ""
                if not is_missing_in_one:
                    len_one = str(len(read_file_as_bytearray(filepath_one)))
                if not is_missing_in_two:
                    len_one = str(len(read_file_as_bytearray(filepath_two)))
                print(f"{filename},,{len_one},{len_two},,")
            continue

        are_equal, len_one, len_two = compare_files(filepath_one, filepath_two)
        div = 0
        if len_two != 0:
            div = round(len_one/len_two, 3)
        if are_equal and print_type not in ("all", "equals"):
            continue
        if not are_equal and print_type not in ("all", "diffs"):
            continue
        print(f"{filename},{are_equal},{len_one},{len_two},{div},{len_one-len_two}")

def main():
    description = ""

    epilog = """\
    """
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("other_baserom", help="Path to the baserom folder that will be compared against.")
    parser.add_argument("filelist", help="Path to filelist to use.")
    parser.add_argument("--print", help="Select what will be printed for a cleaner output. Default is 'all'.", choices=["all", "equals", "diffs", "missing"], default="all")
    parser.add_argument("--csv", help="Print the output in csv format instead.", action="store_true")
    args = parser.parse_args()

    filelist = readFile(args.filelist)

    if args.csv:
        compare_to_csv(args.other_baserom, filelist, args.print)
    else:
        compare_baseroms(args.other_baserom, filelist, args.print)


if __name__ == "__main__":
    main()
