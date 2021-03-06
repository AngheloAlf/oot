#!/usr/bin/python3

from __future__ import annotations

import argparse
import os
import hashlib
import json
import struct
from typing import List
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = script_dir + "/.."
if not script_dir.endswith("/tools"):
    root_dir = script_dir
baserom_path = root_dir + "/baserom_"

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_str_hash(byte_array):
    return str(hashlib.md5(byte_array).hexdigest())

def readFile(filepath):
    with open(filepath) as f:
        return [x.strip() for x in f.readlines()]

def readJson(filepath):
    with open(filepath) as f:
        return json.load(f)

def read_file_as_bytearray(filepath):
    if not os.path.exists(filepath):
        return bytearray(0)
    with open(filepath, mode="rb") as f:
        return bytearray(f.read())

def bytesToBEWords(array_of_bytes: bytearray) -> List[int]:
    words = len(array_of_bytes)//4
    big_endian_format = f">{words}I"
    return list(struct.unpack_from(big_endian_format, array_of_bytes, 0))

def beWordsToBytes(words_list: List[int], buffer: bytearray) -> bytearray:
    words = len(words_list)
    big_endian_format = f">{words}I"
    struct.pack_into(big_endian_format, buffer, 0, *words_list)
    return buffer


class File:
    def __init__(self, array_of_bytes: bytearray):
        self.bytes: bytearray = array_of_bytes
        self.words: List[int] = bytesToBEWords(self.bytes)

    @property
    def size(self):
        return len(self.bytes)
    @property
    def sizew(self):
        return len(self.words)

    def getHash(self):
        return get_str_hash(self.bytes)

    def compareToFile(self, other_file: File, args):
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

            min_len = min(self.sizew, other_file.sizew)
            for i in range(min_len):
                if self.words[i] != other_file.words[i]:
                    result["diff_words"] += 1

        return result

    def blankOutDifferences(self, other: File, args):
        was_updated = False
        if args.ignore80 or args.ignore06:
            min_len = min(self.sizew, other.sizew)
            for i in range(min_len):
                if args.ignore80:
                    if ((self.words[i] >> 24) & 0xFF) == 0x80 and ((other.words[i] >> 24) & 0xFF) == 0x80:
                        self.words[i] = 0x80000000
                        other.words[i] = 0x80000000
                        was_updated = True
                if args.ignore06:
                    if ((self.words[i] >> 24) & 0xFF) == 0x06 and ((other.words[i] >> 24) & 0xFF) == 0x06:
                        self.words[i] = 0x06000000
                        other.words[i] = 0x06000000
                        was_updated = True
        if was_updated:
            self.updateBytes()
            other.updateBytes()

    def updateBytes(self):
        beWordsToBytes(self.words, self.bytes)


class Instruction:
    def __init__(self, instr: int):
        self.opcode = (instr >> 26) & 0x3F
        self.baseRegister = (instr >> 21) & 0x1F # rs
        self.rt = (instr >> 16) & 0x1F # usually the destiny of the operation
        self.immediate = (instr) & 0xFFFF

    @property
    def instr(self):
        return (self.opcode << 26) | (self.baseRegister << 21) | (self.rt << 16) | (self.immediate)

    def isLUI(self) -> bool: # Load Upper Immediate
        return self.opcode == (0x3C >> 2) # 0b001111
    def isADDIU(self) -> bool:
        return self.opcode == (0x24 >> 2) # 0b001001
    def isLW(self) -> bool: # Load Word
        return self.opcode == (0x8C >> 2) # 0b100011
    def isLWCz(self) -> bool: # Load Word to Coprocessor
        if (self.opcode & 0x03) == 0x00:
            return False
        return (self.opcode & 0x3C) == (0xC0 >> 2) # 0b1100zz
    def isANDI(self) -> bool:
        return self.opcode == (0x30 >> 2) # 0b001100
    def isORI(self) -> bool: # Or Immediate
        return self.opcode == (0x34 >> 2) # 0b001101
    def isADDI(self) -> bool:
        return self.opcode == (0x20 >> 2) # 0b001000
    def isDADDI(self) -> bool: # Doubleword add Immediate
        return self.opcode == (0x60 >> 2) # 0b011000
    def isDADDIU(self) -> bool: # Doubleword add Immediate Unsigned
        return self.opcode == (0x64 >> 2) # 0b011001

    def isBEQ(self) -> bool:
        return self.opcode == (0x10 >> 2) # 0b000100
    def isBEQL(self) -> bool:
        return self.opcode == (0x50 >> 2) # 0b010100
    def isBLEZ(self) -> bool:
        return self.opcode == (0x18 >> 2) # 0b000110
    def isBLEZL(self) -> bool:
        return self.opcode == (0x58 >> 2) # 0b010110
    def isBGTZ(self) -> bool:
        return self.opcode == (0x1C >> 2) # 0b000111
    def isBGTZL(self) -> bool:
        return self.opcode == (0x5C >> 2) # 0b010111
    def isBNE(self) -> bool:
        return self.opcode == (0x14 >> 2) # 0b000101
    def isBNEL(self) -> bool:
        return self.opcode == (0x54 >> 2) # 0b010101

    def isJ(self) -> bool: # Jump
        return self.opcode == (0x08 >> 2) # 0b000010
    def isJAL(self) -> bool: # Jump and Link
        return self.opcode == (0x0C >> 2) # 0b000011
    # JALR
    # JR

    def isLB(self) -> bool: # Load Byte
        return self.opcode == (0x80 >> 2) # 0b100000
    def isLBU(self) -> bool: # Load Byte Insigned
        return self.opcode == (0x90 >> 2) # 0b100100

    def isLD(self) -> bool: # Load Doubleword
        return self.opcode == (0xDC >> 2) # 0b110111

    def isLDCz(self) -> bool: # Load Doubleword to Coprocessor z
        if (self.opcode & 0x03) == 0x00:
            return False
        return (self.opcode & 0x3C) == (0xD0 >> 2) # 0b1101zz

    def isLDL(self) -> bool: # Load Doubleword Left
        return self.opcode == (0x68 >> 2) # 0b011010
    def isLDR(self) -> bool: # Load Doubleword Right
        return self.opcode == (0x6C >> 2) # 0b011011

    def isLH(self) -> bool: # Load Halfword
        return self.opcode == (0x84 >> 2) # 0b100001
    def isLHU(self) -> bool: # Load Halfword Unsigned
        return self.opcode == (0x94 >> 2) # 0b100101

    def isLL(self) -> bool: # Load Linked word
        return self.opcode == (0xC0 >> 2) # 0b110000
    def isLLD(self) -> bool: # Load Linked Doubleword
        return self.opcode == (0xD0 >> 2) # 0b110100

    def isLWL(self) -> bool: # Load Word Left
        return self.opcode == (0x88 >> 2) # 0b100010
    def isLWR(self) -> bool: # Load Word Right
        return self.opcode == (0x98 >> 2) # 0b100110

    def isLWU(self) -> bool: # Load Word Unsigned
        return self.opcode == (0x94 >> 2) # 0b100111

    # PREF # Prefetch
    # 0b110011

    def isSB(self) -> bool: # Store Byte
        return self.opcode == (0xA0 >> 2) # 0b101000
    def isSC(self) -> bool: # Store Conditional word
        return self.opcode == (0xE0 >> 2) # 0b111000
    def isSCD(self) -> bool: # Store Conditional Doubleword
        return self.opcode == (0xF0 >> 2) # 0b111100
    def isSD(self) -> bool: # Store Doubleword
        return self.opcode == (0xFC >> 2) # 0b111111

    def isSDCz(self) -> bool: # Store Doubleword from Coprocessor
        if (self.opcode & 0x03) == 0x00:
            return False
        return (self.opcode & 0x3C) == (0xF0 >> 2) # 0b1111zz

    def isSDL(self) -> bool: # Store Doubleword Left
        return self.opcode == (0xB0 >> 2) # 0b101100
    def isSDR(self) -> bool: # Store Doubleword Right
        return self.opcode == (0xB4 >> 2) # 0b101101

    def isCOPz(self) -> bool:
        if (self.opcode & 0x03) == 0x00:
            return False
        return (self.opcode & 0x3C) == (0x40 >> 2) # 0b0100zz

    def isSH(self) -> bool: # Store Halfword
        return self.opcode == (0xA4 >> 2) # 0b101001

    # SLL # Shift word Left Logical
    # SLLV # Shift word Left Logical Variable
    # SLT # Set on Less Than

    def isSLTI(self) -> bool: # Set on Less Than Immediate
        return self.opcode == (0x28 >> 2) # 0b001010
    def isSLTIU(self) -> bool: # Set on Less Than Immediate Unsigned
        return self.opcode == (0x2C >> 2) # 0b001011

    # SLTU # Set on Less Than Unsigned

    # SRA # Shift word Right Arithmetic
    # SRAV # Shift word Right Arithmetic Variable
    # SRL # Shift word Right Logical
    # SRLV # Shift word Right Logical Variable

    # SUB # Subtract word
    # SUBU # Subtract Unsigned word

    def isSW(self) -> bool: # Store Word
        return self.opcode == (0xAC >> 2) # 0b101011
    def isSWCz(self) -> bool: # Store Word from Coprocessor z
        if (self.opcode & 0x03) == 0x00:
            return False
        return (self.opcode & 0x3C) == (0xE0 >> 2) # 0b1110zz

    def isSWL(self) -> bool: # Store Word Left
        return self.opcode == (0xA8 >> 2) # 0b101010
    def isSWR(self) -> bool: # Store Word Right
        return self.opcode == (0xB8 >> 2) # 0b101110

    # XOR # eXclusive OR

    def isXORI(self) -> bool: # eXclusive OR Immediate
        return self.opcode == (0x38 >> 2) # 0b001110

    def isSPECIAL(self) -> bool:
        return self.opcode == 0x00 # 0b000000
    def isREGIMM(self) -> bool:
        return self.opcode == 0x01 # 0b000001

    def sameOpcode(self, other: Instruction) -> bool:
        return self.opcode == other.opcode

    def sameBaseRegister(self, other: Instruction):
        return self.baseRegister == other.baseRegister

    def sameOpcodeButDifferentArguments(self, other: Instruction) -> bool:
        if not self.sameOpcode(other):
            return False
        return self.instr != other.instr

    def blankOut(self):
        self.baseRegister = 0
        self.rt = 0
        self.immediate = 0

    def __str__(self) -> str:
        result = ""
        if self.isLUI():
            result += "LUI"
        elif self.isADDIU():
            result += "ADDIU"
        elif self.isLW():
            result += "LW"
        elif self.isLWCz():
            result += f"LWC{self.opcode&0x3}"
        elif self.isANDI():
            result += "ANDI"
        elif self.isORI():
            result += "ORI"
        elif self.isADDI():
            result += "ADDI"
        elif self.isDADDI():
            result += "DADDI"
        elif self.isDADDIU():
            result += "DADDIU"

        elif self.isBEQ():
            result += "BEQ"
        elif self.isBEQL():
            result += "BEQL"
        elif self.isBLEZ():
            result += "BLEZ"
        elif self.isBLEZL():
            result += "BLEZL"
        elif self.isBGTZ():
            result += "BGTZ"
        elif self.isBGTZL():
            result += "BGTZL"
        elif self.isBNE():
            result += "BNE"
        elif self.isBNEL():
            result += "BNEL"

        elif self.isJ():
            result += "J"
        elif self.isJAL():
            result += "JAL"

        elif self.isLB():
            result += "LB"
        elif self.isLBU():
            result += "LBU"

        elif self.isLD():
            result += "LD"

        elif self.isLDCz():
            result += f"LDC{self.opcode&0x3}"

        elif self.isLDL():
            result += "LDL"
        elif self.isLDR():
            result += "LDR"

        elif self.isLH():
            result += "LH"
        elif self.isLHU():
            result += "LHU"

        elif self.isLL():
            result += "LL"
        elif self.isLLD():
            result += "LLD"

        elif self.isLWL():
            result += "LWL"
        elif self.isLWR():
            result += "LWR"

        elif self.isLWU():
            result += "LWU"

        elif self.isSB():
            result += "SB"
        elif self.isSC():
            result += "SC"
        elif self.isSCD():
            result += "SCD"
        elif self.isSD():
            result += "SD"

        elif self.isSDCz():
            result += f"SDC{self.opcode&0x3}"

        elif self.isSDL():
            result += "SDL"
        elif self.isSDR():
            result += "SDR"

        elif self.isCOPz():
            result += f"COP{self.opcode&0x3}"

        elif self.isSH():
            result += "SH"

        # SLL # Shift word Left Logical
        # SLLV # Shift word Left Logical Variable
        # SLT # Set on Less Than

        elif self.isSLTI():
            result += "SLTI"
        elif self.isSLTIU():
            result += "SLTIU"

        # SLTU # Set on Less Than Unsigned

        # SRA # Shift word Right Arithmetic
        # SRAV # Shift word Right Arithmetic Variable
        # SRL # Shift word Right Logical
        # SRLV # Shift word Right Logical Variable

        # SUB # Subtract word
        # SUBU # Subtract Unsigned word

        elif self.isSW():
            result += "SW"
        elif self.isSWCz():
            result += f"SWC{self.opcode&0x3}"

        elif self.isSWL():
            result += "SWL"
        elif self.isSWR():
            result += "SWR"

        # XOR # eXclusive OR

        elif self.isXORI():
            result += "XORI"

        elif self.isCOPz():
            result += f"COP{self.opcode&0x3}"

        elif self.isSPECIAL():
            result += "SPECIAL"
        elif self.isREGIMM():
            result += "REGIMM"

        else:
            result += hex(self.opcode)
            eprint(f"Unknown opcode: {result}")
        return f"{result} {hex(self.baseRegister)} {hex(self.rt)} {hex(self.immediate)}"

    def __repr__(self) -> str:
        return self.__str__()

class Text(File):
    def __init__(self, array_of_bytes):
        super().__init__(array_of_bytes)

        self.instructions: List[Instruction] = list()
        for word in self.words:
            self.instructions.append(Instruction(word))

    @property
    def nInstr(self):
        return len(self.instructions)

    def compareToFile(self, other: File, args):
        result = super().compareToFile(other, args)

        if isinstance(other, Text):
            result["text"] = {
                "diff_opcode": self.countDiffOpcodes(other),
                "same_opcode_same_args": self.countSameOpcodeButDifferentArguments(other),
            }

        return result

    def countDiffOpcodes(self, other: Text) -> int:
        result = 0
        for i in range(min(self.nInstr, other.nInstr)):
            if not self.instructions[i].sameOpcode(other.instructions[i]):
                result += 1
        return result

    def countSameOpcodeButDifferentArguments(self, other: Text) -> int:
        result = 0
        for i in range(min(self.nInstr, other.nInstr)):
            if self.instructions[i].sameOpcodeButDifferentArguments(other.instructions[i]):
                result += 1
        return result

    def blankOutDifferences(self, other_file: File, args):
        super().blankOutDifferences(other_file, args)
        if not isinstance(other_file, Text):
            return

        was_updated = False

        lui_found = False
        lui_pos = 0
        lui_1_register = 0
        lui_2_register = 0

        for i in range(min(self.nInstr, other_file.nInstr)):
            instr1 = self.instructions[i]
            instr2 = other_file.instructions[i]
            if not lui_found:
                if instr1.isLUI() and instr2.isLUI():
                    lui_found = True
                    lui_pos = i
                    lui_1_register = instr1.rt
                    lui_2_register = instr2.rt
            else:
                if instr1.isADDIU() and instr2.isADDIU():
                    if instr1.baseRegister == lui_1_register and instr2.baseRegister == lui_2_register:
                        instr1.blankOut()
                        instr2.blankOut()
                        self.instructions[lui_pos].blankOut() # lui
                        other_file.instructions[lui_pos].blankOut() # lui
                        lui_found = False
                        was_updated = True
                elif instr1.isLW() and instr2.isLW():
                    if instr1.baseRegister == lui_1_register and instr2.baseRegister == lui_2_register:
                        instr1.blankOut()
                        instr2.blankOut()
                        self.instructions[lui_pos].blankOut() # lui
                        other_file.instructions[lui_pos].blankOut() # lui
                        lui_found = False
                        was_updated = True
                elif instr1.isLWCz():
                    if instr1.baseRegister == lui_1_register and instr2.baseRegister == lui_2_register:
                        instr1.blankOut()
                        instr2.blankOut()
                        self.instructions[lui_pos].blankOut() # lui
                        other_file.instructions[lui_pos].blankOut() # lui
                        lui_found = False
                        was_updated = True
                elif instr1.isORI():
                    if instr1.baseRegister == lui_1_register and instr2.baseRegister == lui_2_register:
                        instr1.blankOut()
                        instr2.blankOut()
                        self.instructions[lui_pos].blankOut() # lui
                        other_file.instructions[lui_pos].blankOut() # lui
                        lui_found = False
                        was_updated = True
            if i > lui_pos + 5:
                lui_found = False

        if was_updated:
            self.updateWords()
            other_file.updateWords()

    def updateWords(self):
        self.words = []
        for instr in self.instructions:
            self.words.append(instr.instr)
        self.updateBytes()


class RelocEntry:
    def __init__(self, entry: int):
        self.sectionId = entry >> 30
        self.relocType = (entry >> 24) & 0x3F
        self.offset = entry & 0x00FFFFFF

class Reloc(File):
    def __init__(self, array_of_bytes):
        super().__init__(array_of_bytes)

        self.entries: List[RelocEntry] = list()
        for word in self.words:
            self.entries.append(RelocEntry(word))

    @property
    def nRelocs(self):
        return len(self.entries)

    def compareToFile(self, other_file: File, args):
        result = super().compareToFile(other_file, args)
        # TODO
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
        self.text = Text(self.bytes[start:end])

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
        self.header = bytesToBEWords(self.bytes[start:end])

        start += header_size
        end += reloc_size
        self.reloc = Reloc(self.bytes[start:end])

        self.tail = bytesToBEWords(self.bytes[end:])


    def compareToFile(self, other_file: File, args):
        result = super().compareToFile(other_file, args)

        if isinstance(other_file, Overlay):
            result["ovl"] = {
                "text": self.text.compareToFile(other_file.text, args),
                "data": self.data.compareToFile(other_file.data, args),
                "rodata": self.rodata.compareToFile(other_file.rodata, args),
                "bss": self.bss.compareToFile(other_file.bss, args),
                "reloc": self.reloc.compareToFile(other_file.reloc, args),
            }

        return result

    def blankOutDifferences(self, other_file: File, args):
        super().blankOutDifferences(other_file, args)
        if not isinstance(other_file, Overlay):
            return

        self.text.blankOutDifferences(other_file.text, args)

        self.words = self.text.words + self.data.words + self.rodata.words + self.bss.words + self.header + self.reloc.words + self.tail
        self.updateBytes()
        
        other_file.words = other_file.text.words + other_file.data.words  + other_file.rodata.words + other_file.bss.words + other_file.header + other_file.reloc.words + other_file.tail
        other_file.updateBytes()

    def relocate(self, allocatedVRamAddress: int, vRamAddress: int):
        allocu32 = allocatedVRamAddress

        sections = [0, 0, 0, 0]
        sections[0] = 0
        sections[1] = allocu32
        sections[2] = allocu32 + self.text.size
        sections[3] = sections[2] + self.data.size

        for reloc in self.reloc.entries:
            relocDataPtr = reloc.sectionId
            # relocData = *relocDataPtr
            if reloc.relocType == 2:
                pass
            elif reloc.relocType == 4:
                pass
            elif reloc.relocType == 5:
                pass
            elif reloc.relocType == 6:
                pass


def print_result_different(comparison, indentation=0):
    if comparison['size_one'] != comparison['size_two']:
        div = round(comparison['size_two']/comparison['size_one'], 3)
        print((indentation * "\t") + f"Size doesn't match: {comparison['size_one']} vs {comparison['size_two']} (x{div}) ({comparison['size_two'] - comparison['size_one']})")
    else:
        print((indentation * "\t") + "Size matches.")
    print((indentation * "\t") + f"There are at least {comparison['diff_bytes']} bytes different, and {comparison['diff_words']} words different.")

def compare_baseroms(args, filelist):
    missing_in_one = set()
    missing_in_two = set()

    equals = 0
    different = 0

    for filename in filelist:
        filepath_one = os.path.join(baserom_path + args.version1, filename)
        filepath_two = os.path.join(baserom_path + args.version2, filename)

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

        if filename.startswith("ovl_"):
            file_one = Overlay(file_one_data)
            file_two = Overlay(file_two_data)
        else:
            file_one = File(file_one_data)
            file_two = File(file_two_data)

        file_one.blankOutDifferences(file_two, args)

        comparison = file_one.compareToFile(file_two, args)

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
    index = -1

    column1 = args.version1 if args.column1 is None else args.column1
    column2 = args.version2 if args.column2 is None else args.column2

    print(f"Index,File,Are equals,Size in {column1},Size in {column2},Size proportion,Size difference,Bytes different,Words different", end="")
    if args.overlays:
        print(",Opcodes difference,Same opcode but different arguments", end="")
    print(flush=True)

    for filename in filelist:
        filepath_one = os.path.join(baserom_path + args.version1, filename)
        filepath_two = os.path.join(baserom_path + args.version2, filename)

        index += 1

        #if args.filetype != "all" and args.filetype != filedata["type"]:
        #    continue

        file_one_data = read_file_as_bytearray(filepath_one)
        file_two_data = read_file_as_bytearray(filepath_two)

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
            if filename.startswith("ovl_"):
                file_one = Overlay(file_one_data)
                file_two = Overlay(file_two_data)
            else:
                file_one = File(file_one_data)
                file_two = File(file_two_data)

            file_one.blankOutDifferences(file_two, args)

            comparison = file_one.compareToFile(file_two, args)
            equal = comparison["equal"]

            if equal and args.print not in ("all", "equals"):
                continue
            if not equal and args.print not in ("all", "diffs"):
                continue
            len_one = comparison["size_one"]
            len_two = comparison["size_two"]
            if len_one > 0:
                div = round(len_two/len_one, 3)
            else:
                div = "Inf"
            size_difference = len_two - len_one
            diff_bytes = comparison["diff_bytes"]
            diff_words = comparison["diff_words"]

        if args.overlays and len(comparison) > 0 and "ovl" in comparison:
            for section_name in comparison["ovl"]:
                section = comparison["ovl"][section_name]
                equal = section["equal"]

                if equal and args.print not in ("all", "equals"):
                    continue
                if not equal and args.print not in ("all", "diffs"):
                    continue

                len_one = section["size_one"]
                len_two = section["size_two"]
                if len_one > 0 or len_two > 0:
                    if len_one > 0:
                        div = round(len_two/len_one, 3)
                    else:
                        div = "Inf"
                    size_difference = len_two - len_one
                    diff_bytes = section["diff_bytes"]
                    diff_words = section["diff_words"]
                    print(f'{index},{filename} {section_name},{equal},{len_one},{len_two},{div},{size_difference},{diff_bytes},{diff_words}', end="")
                    if "text" in section:
                        print(f',{section["text"]["diff_opcode"]},{section["text"]["same_opcode_same_args"]}', end="")
                    else:
                        print(",,", end="")
                    print()
        else:
            print(f'{index},{filename},{equal},{len_one},{len_two},{div},{size_difference},{diff_bytes},{diff_words}', end="")
            if args.overlays:
                print(",,", end="")
            print()


def main():
    description = ""

    epilog = """\
    """
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("version1", help="A version of the game to compare. The files will be read from baserom_version1. For example: baserom_pal_mq_dbg")
    parser.add_argument("version2", help="A version of the game to compare. The files will be read from baserom_version2. For example: baserom_pal_mq")
    parser.add_argument("filelist", help="Path to filelist to use.")
    parser.add_argument("--print", help="Select what will be printed for a cleaner output. Default is 'all'.", choices=["all", "equals", "diffs", "missing"], default="all")
    # parser.add_argument("--filetype", help="Filters by filetype. Default: all",  choices=["all", "Unknown", "Overlay", "Object", "Texture", "Room", "Scene", "Other"], default="all")
    parser.add_argument("--overlays", help="Treats each section of the overalays as separate files.", action="store_true")
    parser.add_argument("--csv", help="Print the output in csv format instead.", action="store_true")
    #parser.add_argument("--ignore80", help="Ignores words differences that starts in 0x80XXXXXX", action="store_true")
    parser.add_argument("--ignore80", help="Ignores words differences that starts in 0x80XXXXXX", action="store_true", default=True) # temporal?
    parser.add_argument("--ignore06", help="Ignores words differences that starts in 0x06XXXXXX", action="store_true")
    parser.add_argument("--column1", help="Name for column one (baserom) in the csv.", default=None)
    parser.add_argument("--column2", help="Name for column two (other_baserom) in the csv.", default=None)
    args = parser.parse_args()

    filelist = readFile(args.filelist)
    # filelist = readJson(args.filelist)

    if args.csv:
        compare_to_csv(args, filelist)
    else:
        compare_baseroms(args, filelist)


if __name__ == "__main__":
    main()
