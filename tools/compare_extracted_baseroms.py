#!/usr/bin/python3

from __future__ import annotations

import argparse
import os
import hashlib
import struct

script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = script_dir + "/.."
if not script_dir.endswith("/tools"):
    root_dir = script_dir
baserom_path = root_dir + "/baserom_"


def get_str_hash(byte_array):
    return str(hashlib.md5(byte_array).hexdigest())

def readFile(filepath):
    with open(filepath) as f:
        return [x.strip() for x in f.readlines()]

def read_file_as_bytearray(filepath):
    with open(filepath, mode="rb") as f:
        return bytearray(f.read())

def compare_files(filepath_one, filepath_two, args):
    file_one = read_file_as_bytearray(filepath_one)
    file_two = read_file_as_bytearray(filepath_two)
    are_equal = get_str_hash(file_one) == get_str_hash(file_two)
    len_one = len(file_one)
    len_two = len(file_two)
    diff_bytes = 0
    diff_words = 0

    if not are_equal:
        min_len = min(len_one, len_two)
        for i in range(min_len):
            if file_one[i] != file_two[i]:
                diff_bytes += 1

        words = str(min_len//4)
        big_endian_format = ">" + words + "I"
        file_one_words = struct.unpack_from(big_endian_format, file_one, 0)
        file_two_words = struct.unpack_from(big_endian_format, file_two, 0)
        for i in range(min_len//4):
            if file_one_words[i] != file_two_words[i]:
                if args.ignore80:
                    if ((file_one_words[i] >> 24) & 0xFF) == 0x80 and ((file_two_words[i] >> 24) & 0xFF) == 0x80:
                        continue
                if args.ignore06:
                    if ((file_one_words[i] >> 24) & 0xFF) == 0x06 and ((file_two_words[i] >> 24) & 0xFF) == 0x06:
                        continue
                diff_words += 1

    return are_equal, len_one, len_two, diff_bytes, diff_words


def compare_baseroms(args, filelist):
    files_baserom_one = set()
    files_baserom_two = set()

    missing_in_one = set()
    missing_in_two = set()

    equals = 0
    different = 0

    for filename in filelist:
        filepath_one = os.path.join(baserom_path + args.version1, filename)
        filepath_two = os.path.join(baserom_path + args.version2, filename)

        is_missing = False

        if os.path.exists(filepath_one):
            files_baserom_one.add(filename)
        else:
            missing_in_one.add(filename)
            is_missing = True
            if args.print in ("all", "missing"):
                print(f"File {filename} does not exists in baserom.")

        if os.path.exists(filepath_two):
            files_baserom_two.add(filename)
        else:
            missing_in_two.add(filename)
            is_missing = True
            if args.print in ("all", "missing"):
                print(f"File {filename} does not exists in other_baserom.")

        if is_missing:
            continue

        are_equal, len_one, len_two, diff_bytes, diff_words = compare_files(filepath_one, filepath_two, args)
        if are_equal:
            equals += 1
            if args.print in ("all", "equals"):
                print(f"{filename} OK")
        else:
            different += 1
            if args.print in ("all", "diffs"):
                print(f"{filename} not OK")
                if len_one != len_two:
                    div = round(len_two/len_two, 3)
                    print(f"\tSize doesn't match: {len_one} vs {len_two} (x{div}) ({len_two-len_one})")
                else:
                    print("\tSize matches.")
                print(f"\tThere are at least {diff_bytes} bytes different, and {diff_words} words different.")

    total = len(filelist)
    if total > 0:
        print()
        if args.print in ("all", "equals"):
            print(f"Equals:     {equals}/{total} ({round(100*equals/total, 2)}%)")
        if args.print in ("all", "diffs"):
            print(f"Differents: {different}/{total} ({round(100*different/total, 2)}%)")
        if args.print in ("all", "missing"):
            missing = len(missing_in_one)
            print(f"Missing:    {missing}/{total} ({round(100*missing/total, 2)}%)")
            print(f"Missing 2:  {len(missing_in_two)}")

def compare_to_csv(args, filelist):
    files_baserom_one = set()
    files_baserom_two = set()

    missing_in_one = set()
    missing_in_two = set()

    index = -1

    column1 = args.version1 if args.column1 is None else args.column1
    column2 = args.version2 if args.column2 is None else args.column2

    print(f"Index,File,Are equals,Size in {column1},Size in {column2},Size proportion,Size difference,Bytes different,Words different")

    for filename in filelist:
        filepath_one = os.path.join(baserom_path + args.version1, filename)
        filepath_two = os.path.join(baserom_path + args.version2, filename)
        is_missing_in_one = False
        is_missing_in_two = False

        index += 1

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
            if args.print in ("all", "missing"):
                len_one = ""
                len_two = ""
                if not is_missing_in_one:
                    len_one = str(len(read_file_as_bytearray(filepath_one)))
                if not is_missing_in_two:
                    len_two = str(len(read_file_as_bytearray(filepath_two)))
                print(f"{index},{filename},,{len_one},{len_two},,,")
            continue

        are_equal, len_one, len_two, diff_bytes, diff_words = compare_files(filepath_one, filepath_two, args)
        div = 0
        if len_two != 0:
            div = round(len_one/len_two, 3)
        if are_equal and args.print not in ("all", "equals"):
            continue
        if not are_equal and args.print not in ("all", "diffs"):
            continue
        print(f"{index},{filename},{are_equal},{len_one},{len_two},{div},{len_one-len_two},{diff_bytes},{diff_words}")


def main():
    description = ""

    epilog = """\
    """
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("version1", help="A version of the game to compare. The files will be read from baserom_version1. For example: baserom_pal_mq_dbg")
    parser.add_argument("version2", help="A version of the game to compare. The files will be read from baserom_version2. For example: baserom_pal_mq")
    parser.add_argument("filelist", help="Path to filelist to use.")
    parser.add_argument("--print", help="Select what will be printed for a cleaner output. Default is 'all'.", choices=["all", "equals", "diffs", "missing"], default="all")
    parser.add_argument("--csv", help="Print the output in csv format instead.", action="store_true")
    parser.add_argument("--ignore80", help="Ignores words differences that starts in 0x80XXXXXX", action="store_true")
    parser.add_argument("--ignore06", help="Ignores words differences that starts in 0x06XXXXXX", action="store_true")
    parser.add_argument("--column1", help="Name for column one (version1) in the csv.", default=None)
    parser.add_argument("--column2", help="Name for column two (version2) in the csv.", default=None)
    args = parser.parse_args()

    filelist = readFile(args.filelist)

    if args.csv:
        compare_to_csv(args, filelist)
    else:
        compare_baseroms(args, filelist)


if __name__ == "__main__":
    main()
