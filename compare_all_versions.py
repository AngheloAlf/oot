#!/usr/bin/python3

from __future__ import annotations

import argparse
import os
import hashlib
import json
import struct
from typing import List
import sys
import subprocess

# Returns the md5 hash of a bytearray
def getStrHash(byte_array: bytearray) -> str:
    return str(hashlib.md5(byte_array).hexdigest())

def readFileAsBytearray(filepath: str) -> bytearray:
    if not os.path.exists(filepath):
        return bytearray(0)
    with open(filepath, mode="rb") as f:
        return bytearray(f.read())

def readFile(filepath: str):
    with open(filepath) as f:
        return [x.strip() for x in f.readlines()]

def runCommandGetOutput(command: str, args: List[str]) -> List[str] | None:
    try:
        output = subprocess.check_output([command, *args]).decode("utf-8")
        return output.strip().split("\n")
    except:
        return None

def removeExtraWhitespace(line: str) -> str:
    return" ".join(line.split()) 


versions = {
    "ntsc_0.9" : "NNR",
    "ntsc_1.0" : "NN0",
    "ntsc_1.1" : "NN1",
    "pal_1.0" : "NP0",
    "ntsc_1.2" : "NN2",
    "pal_1.1" : "NP1",
    "jp_gc" : "GJO",
    "jp_mq" : "GJM",
    "usa_gc" : "GUO",
    "usa_mq" : "GUM",
    "pal_gc" : "GPO",
    "pal_gc_dbg" : "GPOD",
    "pal_mq" : "GPM",
    "pal_mq_dbg" : "GPMD",
    "jp_gc_ce" : "GJC",
}

def getVersionAbbr(filename: str) -> str:
    for ver in versions:
        if "baserom_" + ver + "/" in filename:
            return versions[ver]
    # If the version wasn't found.
    return filename

def countUnique(row: list) -> int:
    unique = set(row)
    count = len(unique)
    if "" in unique:
        count -= 1
    return count


def compareFileAcrossVersions(versionsList: List[str], filename: str):
    md5arglist = list(map(lambda orig_string: "baserom_" + orig_string + "/" + filename, versionsList))
    # os.system( "md5sum " + " ".join(md5arglist) )

    # Get hashes.
    output = runCommandGetOutput("md5sum", md5arglist)

    # Print md5hash
    #print("\n".join(output))
    #print()

    filesHashes = dict() # "NN0": "339614255f179a1e308d954d8f7ffc0a"
    firstFilePerHash = dict() # "339614255f179a1e308d954d8f7ffc0a": "NN0"

    for line in output:
        trimmed = removeExtraWhitespace(line)
        filehash, filename = trimmed.split(" ")
        abbr = getVersionAbbr(filename)
        
        # Map each abbreviation and its hash.
        filesHashes[abbr] = filehash

        # Find out where in which version this hash appeared for first time.
        if filehash not in firstFilePerHash:
            firstFilePerHash[filehash] = abbr

    row = []
    for ver in versionsList:
        abbr = versions[ver]

        if abbr in filesHashes:
            fHash = filesHashes[abbr]
            row.append(firstFilePerHash[fHash])
        else:
            row.append("")
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("versionlist", help="Path to version list.")
    parser.add_argument("filelist", help="List of filenames of the ROM that will be compared.")
    parser.add_argument("--noheader", help="Disables the csv header.", action="store_true")
    args = parser.parse_args()

    lines = open(args.versionlist).read().splitlines()
    filesList = readFile(args.filelist)

    if not args.noheader:
        # Print csv header
        print("Object name", end="")
        for ver in lines:
            print("," + ver, end="")
        print(",Different versions", end="")
        print()

    for filename in filesList:
        row = compareFileAcrossVersions(lines, filename)

        # Print csv row
        print(filename, end="")
        for cell in row:
            print("," + cell, end="")
        print("," + str(countUnique(row)), end="")
        print()

if __name__ == "__main__":
    main()
