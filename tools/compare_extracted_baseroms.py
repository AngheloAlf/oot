#!/usr/bin/python3

from __future__ import annotations

import argparse
import os
import hashlib
import json
import struct

script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = script_dir + "/.."
if not script_dir.endswith("/tools"):
    root_dir = script_dir
baserom_path = root_dir + "/baserom"


def get_str_hash(byte_array):
    return str(hashlib.md5(byte_array).hexdigest())

def readJson(filepath):
    with open(filepath) as f:
        return json.load(f)

def read_file_as_bytearray(filepath):
    if not os.path.exists(filepath):
        return bytearray(0)
    with open(filepath, mode="rb") as f:
        return bytearray(f.read())


class File:
    def __init__(self, array_of_bytes):
        self.bytes = array_of_bytes
        self.size = len(self.bytes)
        words = str(self.size//4)
        big_endian_format = ">" + words + "I"
        self.words = struct.unpack_from(big_endian_format, self.bytes, 0)

    def getHash(self):
        return get_str_hash(self.bytes)

    def compareToFile(self, other_file: File):
        hash_one = self.getHash()
        hash_two = other_file.getHash()

        result = {
            "equal": hash_one == hash_two,
            "hash_one": hash_one,
            "hash_two": hash_two,
            "size_one": self.size,
            "size_two": other_file.size,
            "diff_bytes": 0,
            "diff_words": 0,
        }

        if not result["equal"]:
            min_len = min(self.size, other_file.size)
            for i in range(min_len):
                if self.bytes[i] != other_file.bytes[i]:
                    result["diff_bytes"] += 1

            for i in range(min_len//4):
                if self.words[i] != other_file.words[i]:
                    result["diff_words"] += 1

        return result


class Overlay(File):
    def __init__(self, array_of_bytes):
        super().__init__(array_of_bytes)

        seekup = self.words[-1]
        self.headerBPos = self.size - seekup
        self.headerWPos = self.headerBPos//4
        
        text_size = self.words[self.headerWPos]
        data_size = self.words[self.headerWPos+1]
        rodata_size = self.words[self.headerWPos+2]
        bss_size = self.words[self.headerWPos+3]
        header_size = 4*5
        reloc_size = 4*self.words[self.headerWPos+4]

        start = 0
        end = text_size
        self.text = File(self.bytes[start:end])

        start += text_size
        end += data_size
        self.data = File(self.bytes[start:end])

        start += data_size
        end += rodata_size
        self.rodata = File(self.bytes[start:end])

        start += rodata_size
        end += bss_size
        self.bss = File(self.bytes[start:end])

        start += bss_size
        end += header_size
        self.header = self.bytes[start:end]

        start += header_size
        end += reloc_size
        self.reloc = File(self.bytes[start:end])

    def compareToFile(self, other_file: File):
        result = super().compareToFile(other_file)

        if isinstance(other_file, Overlay):
            result["ovl"] = {
                "text": self.text.compareToFile(other_file.text),
                "data": self.data.compareToFile(other_file.data),
                "rodata": self.rodata.compareToFile(other_file.rodata),
                "bss": self.bss.compareToFile(other_file.bss),
                "reloc": self.reloc.compareToFile(other_file.reloc),
            }

        return result


def print_result_different(comparison, indentation=0):
    if comparison['size_one'] != comparison['size_two']:
        div = round(comparison['size_one']/comparison['size_two'], 3)
        print((indentation * "\t") + f"Size doesn't match: {comparison['size_one']} vs {comparison['size_two']} (x{div}) ({comparison['size_one'] - comparison['size_two']})")
    else:
        print((indentation * "\t") + "Size matches.")
    print((indentation * "\t") + f"There are at least {comparison['diff_bytes']} bytes different, and {comparison['diff_words']} words different.")

def compare_baseroms(args, filelist):
    missing_in_one = set()
    missing_in_two = set()

    equals = 0
    different = 0

    for filedata in filelist["files"]:
        filename = filedata["name"]
        filepath_one = os.path.join(baserom_path, filename)
        filepath_two = os.path.join(args.other_baserom, filename)

        if args.filetype != "all" and args.filetype != filedata["type"]:
            continue

        if not os.path.exists(filepath_one):
            missing_in_one.add(filename)
            if args.print in ("all", "missing"):
                print(f"File {filename} does not exists in baserom.")
            continue

        if not os.path.exists(filepath_two):
            missing_in_two.add(filename)
            if args.print in ("all", "missing"):
                print(f"File {filename} does not exists in other_baserom.")
            continue

        file_one_data = read_file_as_bytearray(filepath_one)
        file_two_data = read_file_as_bytearray(filepath_two)

        if filedata["type"] == "Overlay":
            file_one = Overlay(file_one_data)
            file_two = Overlay(file_two_data)
        else:
            file_one = File(file_one_data)
            file_two = File(file_two_data)

        comparison = file_one.compareToFile(file_two)

        if comparison["equal"]:
            equals += 1
            if args.print in ("all", "equals"):
                print(f"{filename} OK")
        else:
            different += 1
            if args.print in ("all", "diffs"):
                print(f"{filename} not OK")
                print_result_different(comparison, 1)
                
                if "ovl" in comparison:
                    for section_name in comparison["ovl"]:
                        section = comparison["ovl"][section_name]

                        if section["size_one"] == 0:
                            continue        

                        if section["equal"] and args.print in ("all", "equals"):
                            print(f"\t\t{section_name} OK")
                        else:
                            print(f"\t\t{section_name} not OK")
                            print_result_different(section, 3)

    total = len(filelist["files"])
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
    index = -1

    print(f"Index,File,Are equals,Size in {args.column1},Size in {args.column2},Size proportion,Size difference,Bytes different,Words different", end="")
    if args.filetype == "Overlay":
        print(f",text: Size in {args.column1},Size in {args.column2},Size difference,Words different", end="")
        print(f",data: Size in {args.column1},Size in {args.column2},Size difference,Words different", end="")
        print(f",rodata: Size in {args.column1},Size in {args.column2},Size difference,Words different", end="")

    print()

    for filedata in filelist["files"]:
        filename = filedata["name"]
        index += 1

        if args.filetype != "all" and args.filetype != filedata["type"]:
            continue

        file_one_data = read_file_as_bytearray(os.path.join(baserom_path, filename))
        file_two_data = read_file_as_bytearray(os.path.join(args.other_baserom, filename))

        equal = ""
        len_one = ""
        len_two = ""
        div = ""
        size_difference = ""
        diff_bytes = ""
        diff_words = ""
        comparison = dict()

        is_missing_in_one = len(file_one_data) == 0
        is_missing_in_two = len(file_two_data) == 0

        if is_missing_in_one or is_missing_in_two:
            if args.print not in ("all", "missing"):
                continue
            len_one = "" if is_missing_in_one else len(file_one_data)
            len_two = "" if is_missing_in_two else len(file_two_data)

        else:
            if filedata["type"] == "Overlay":
                file_one = Overlay(file_one_data)
                file_two = Overlay(file_two_data)
            else:
                file_one = File(file_one_data)
                file_two = File(file_two_data)

            comparison = file_one.compareToFile(file_two)

            if comparison["equal"] and args.print not in ("all", "equals"):
                continue
            if not comparison["equal"] and args.print not in ("all", "diffs"):
                continue

            equal = comparison["equal"]
            len_one = comparison["size_one"]
            len_two = comparison["size_two"]
            div = round(comparison["size_one"]/comparison["size_two"], 3)
            size_difference = comparison["size_one"]-comparison["size_two"]
            diff_bytes = comparison["diff_bytes"]
            diff_words = comparison["diff_words"]

        print(f'{index},{filename},{equal},{len_one},{len_two},{div},{size_difference},{diff_bytes},{diff_words}', end="")
        if filedata["type"] == "Overlay" and len(comparison) > 0:
            for section_name in ["text", "data", "rodata"]:
                section = comparison["ovl"][section_name]
                len_one = section["size_one"]
                len_two = section["size_two"]
                diff_words = section["diff_words"]
                print(f',{len_one},{len_two},{len_one-len_two},{diff_words}', end="")
        print()


def main():
    description = ""

    epilog = """\
    """
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("other_baserom", help="Path to the baserom folder that will be compared against.")
    parser.add_argument("filelist", help="Path to filelist to use.")
    parser.add_argument("--print", help="Select what will be printed for a cleaner output. Default is 'all'.", choices=["all", "equals", "diffs", "missing"], default="all")
    parser.add_argument("--filetype", help="Filters by filetype. Default: all",  choices=["all", "Unknown", "Overlay", "Object", "Texture", "Room", "Scene", "Other"], default="all")
    parser.add_argument("--csv", help="Print the output in csv format instead.", action="store_true")
    parser.add_argument("--column1", help="Name for column one (baserom) in the csv.", default="baserom")
    parser.add_argument("--column2", help="Name for column two (other_baserom) in the csv.", default="other_baserom")
    args = parser.parse_args()

    filelist = readJson(args.filelist)

    if args.csv:
        compare_to_csv(args, filelist)
    else:
        compare_baseroms(args, filelist)


if __name__ == "__main__":
    main()
