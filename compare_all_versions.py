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

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Returns the md5 hash of a bytearray
def getStrHash(byte_array: bytearray) -> str:
    return str(hashlib.md5(byte_array).hexdigest())

def writeBytearrayToFile(filepath: str, array_of_bytes: bytearray):
    with open(filepath, mode="wb") as f:
       f.write(array_of_bytes)

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
        return getStrHash(self.bytes)

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
                    #if isinstance(self, Text) and isinstance(other_file, Text):
                        #eprint(f"Differing instruction: {self.instructions[i]}")
                        #eprint(f"Differing instruction: {other_file.instructions[i]}")
                        #eprint(f"")
                        #pass

        return result

    def blankOutDifferences(self, other: File, args):
        was_updated = False
        if args.ignore80 or args.ignore06 or args.ignore04:
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
                if args.ignore04:
                    if ((self.words[i] >> 24) & 0xFF) == 0x04 and ((other.words[i] >> 24) & 0xFF) == 0x04:
                        self.words[i] = 0x04000000
                        other.words[i] = 0x04000000
                        was_updated = True
        if was_updated:
            self.updateBytes()
            other.updateBytes()

    def removePointers(self):
        pass

    def updateBytes(self):
        beWordsToBytes(self.words, self.bytes)

    def saveToFile(self, filepath: str):
        writeBytearrayToFile(filepath, self.bytes)


class Instruction:
    NormalOpcodes = {
        0b000_000: "SPECIAL",
        0b000_001: "REGIMM",
        0b000_010: "J", # Jump
        0b000_011: "JAL", # Jump and Link
        0b000_100: "BEQ",
        0b000_101: "BNE",
        0b000_110: "BLEZ",
        0b000_111: "BGTZ",

        0b001_000: "ADDI", # Add Immediate
        0b001_001: "ADDIU", # Add Immediate Unsigned Word
        0b001_010: "SLTI", # Set on Less Than Immediate
        0b001_011: "SLTIU", # Set on Less Than Immediate Unsigned
        0b001_100: "ANDI", # And Immediate
        0b001_101: "ORI", # Or Immediate
        0b001_110: "XORI", # eXclusive OR Immediate
        0b001_111: "LUI", # Load Upper Immediate

        0b010_000: "COP0", # Coprocessor OPeration z
        0b010_001: "COP1", # Coprocessor OPeration z
        0b010_010: "COP2", # Coprocessor OPeration z
        0b010_011: "COP1X", # Coprocessor OPeration z
        0b010_100: "BEQL",
        0b010_101: "BNEL",
        0b010_110: "BLEZL",
        0b010_111: "BGTZL",

        0b011_000: "DADDI", # Doubleword add Immediate
        0b011_001: "DADDIU", # Doubleword add Immediate Unsigned
        0b011_010: "LDL", # Load Doubleword Left
        0b011_011: "LDR", # Load Doubleword Right
        # 0b011_100: "",
        # 0b011_101: "",
        # 0b011_110: "",
        # 0b011_111: "",

        0b100_000: "LB", # Load Byte
        0b100_001: "LH", # Load Halfword
        0b100_010: "LWL", # Load Word Left
        0b100_011: "LW", # Load Word
        0b100_100: "LBU", # Load Byte Insigned
        0b100_101: "LHU", # Load Halfword Unsigned
        0b100_110: "LWR", # Load Word Right
        0b100_111: "LWU", # Load Word Unsigned

        0b101_000: "SB", # Store Byte
        0b101_001: "SH", # Store Halfword
        0b101_010: "SWL", # Store Word Left
        0b101_011: "SW", # Store Word
        0b101_100: "SDL", # Store Doubleword Left
        0b101_101: "SDR", # Store Doubleword Right
        0b101_110: "SWR", # Store Word Right
        # 0b101_111: "",

        0b110_000: "LL", # Load Linked word
        0b110_001: "LWC1", # Load Word to Coprocessor z
        0b110_010: "LWC2", # Load Word to Coprocessor z
        0b110_011: "PREF", # Prefetch
        0b110_100: "LLD", # Load Linked Doubleword
        0b110_101: "LDC1", # Load Doubleword to Coprocessor z
        0b110_110: "LDC2", # Load Doubleword to Coprocessor z
        0b110_111: "LD", # Load Doubleword

        0b111_000: "SC", # Store Conditional word
        0b111_001: "SWC1", # Store Word from Coprocessor z
        0b111_010: "SWC2", # Store Word from Coprocessor z
        # 0b111_011: "",
        0b111_100: "SCD", # Store Conditional Doubleword
        0b111_101: "SDC1", # Store Doubleword from Coprocessor z
        0b111_110: "SDC2", # Store Doubleword from Coprocessor z
        0b111_111: "SD", # Store Doubleword
    }

    def __init__(self, instr: int):
        self.opcode = (instr >> 26) & 0x3F
        self.rs = (instr >> 21) & 0x1F # rs
        self.rt = (instr >> 16) & 0x1F # usually the destiny of the operation
        self.rd = (instr >> 11) & 0x1F # destination register in R-Type instructions
        self.sa = (instr >>  6) & 0x1F
        self.function = (instr >> 0) & 0x3F

    @property
    def instr(self) -> int:
        return (self.opcode << 26) | (self.rs << 21) | (self.rt << 16) | (self.immediate)

    @property
    def immediate(self) -> int:
        return (self.rd << 11) | (self.sa << 6) | (self.function)
    @property
    def instr_index(self) -> int:
        return (self.rs << 21) | (self.rt << 16) | (self.immediate)
    @property
    def baseRegister(self) -> int:
        return self.rs

    def isBranch(self) -> bool:
        opcode = self.getOpcodeName()
        if opcode == "J" or opcode == "JAL":
            return True
        if opcode == "BEQ" or opcode == "BEQL":
            return True
        if opcode == "BLEZ" or opcode == "BLEZL":
            return True
        if opcode == "BNE" or opcode == "BNEL":
            return True
        return False

    def isJType(self) -> bool: # OP LABEL
        opcode = self.getOpcodeName()
        return opcode == "J" or opcode == "JAL"
    def isRType(self) -> bool: # OP rd, rs, rt
        return False
    def isIType(self) -> bool: # OP rt, IMM(rs)
        if self.isJType():
            return False
        if self.isRType():
            return False
        if self.isIType2():
            return False
        if self.isIType3():
            return False
        return True
    def isIType2(self) -> bool: # OP  rs, rt, IMM
        opcode = self.getOpcodeName()
        if opcode == "BEQ" or opcode == "BEQL":
            return True
        if opcode == "BNE" or opcode == "BNEL":
            return True
        return False
    def isIType3(self) -> bool: # OP  rt, rs, IMM
        opcode = self.getOpcodeName()
        if opcode == "ADDI" or opcode == "ADDIU":
            return True
        if opcode == "ANDI":
            return True
        if opcode == "DADDI" or opcode == "DADDIU":
            return True
        if opcode == "ORI" or opcode == "XORI":
            return True
        if opcode == "SLTI" or opcode == "SLTIU":
            return True
        return False

    def sameOpcode(self, other: Instruction) -> bool:
        return self.opcode == other.opcode

    def sameBaseRegister(self, other: Instruction):
        return self.baseRegister == other.baseRegister

    def sameOpcodeButDifferentArguments(self, other: Instruction) -> bool:
        if not self.sameOpcode(other):
            return False
        return self.instr != other.instr

    def blankOut(self):
        self.rs = 0
        self.rt = 0
        self.rd = 0
        self.sa = 0
        self.function = 0

    def getOpcodeName(self) -> str:
        opcode = "0x" + hex(self.opcode).strip("0x").zfill(2)
        return Instruction.NormalOpcodes.get(self.opcode, f"({opcode})")

    def getRegisterName(self, register: int) -> str:
        if register == 0:
            return "$zero"
        elif register == 1:
            return "$at"
        elif 2 <= register <= 3:
            return "$v" + str(register-2)
        elif 4 <= register <= 7:
            return "$a" + str(register-4)
        elif 8 <= register <= 15:
            return "$t" + str(register-8)
        elif 16 <= register <= 23:
            return "$s" + str(register-16)
        elif 24 <= register <= 25:
            return "$t" + str(register-24)
        elif 26 <= register <= 27:
            return "$k" + str(register-26)
        elif register == 28:
            return "$gp"
        elif register == 29:
            return "$sp"
        elif register == 30:
            return "$fp"
        elif register == 31:
            return "$ra"
        return hex(register)

    def getFloatRegisterName(self, register: int) -> str:
        if 0 <= register <= 31:
            return "$f" + str(register)
        return hex(register)

    def __str__(self) -> str:
        if self.instr == 0:
            return "nop"

        opcode = self.getOpcodeName().lower().ljust(7, ' ')
        rs = self.getRegisterName(self.rs)
        rt = self.getRegisterName(self.rt)
        immediate = "0x" + hex(self.immediate).strip("0x").zfill(4).upper()

        if self.isIType():
            result = f"{opcode} {rt},"
            result = result.ljust(14, ' ')
            return f"{result} {immediate}({rs})"
        elif self.isIType2():
            result = f"{opcode} {rs},"
            result = result.ljust(14, ' ')
            result += f" {rt},"
            result = result.ljust(19, ' ')
            return f"{result} {immediate}"
        elif self.isIType3():
            result = f"{opcode} {rt},"
            result = result.ljust(14, ' ')
            result += f" {rs},"
            result = result.ljust(19, ' ')
            return f"{result} {immediate}"
        elif self.isJType():
            instr_index = "0x" + hex(self.instr_index).strip("0x").zfill(7).upper()
            return f"{opcode} {instr_index}"
        elif self.isRType():
            rd = self.getRegisterName(self.rd)
            result = f"{opcode} {rd},"
            result = result.ljust(14, ' ')
            result += f" {rs},"
            result = result.ljust(19, ' ')
            return f"{result} {rt}"
        return "ERROR"

    def __repr__(self) -> str:
        return self.__str__()

class InstructionSpecial(Instruction):
    SpecialOpcodes = {
        0b000_000: "SLL", # Shift word Left Logical
        0b000_001: "MOVCI",
        0b000_010: "SRL", # Shift word Right Logical
        0b000_011: "SRA", # Shift word Right Arithmetic
        0b000_100: "SLLV", # Shift word Left Logical Variable
        # 0b000_101: "",
        0b000_110: "SRLV", # Shift word Right Logical Variable
        0b000_111: "SRAV", # Shift word Right Arithmetic Variable

        0b001_000: "JR", # Jump Register
        0b001_001: "JALR", # Jump And Link Register
        0b001_010: "MOVZ",
        0b001_011: "MOVN",
        0b001_100: "SYSCALL",
        0b001_101: "BREAK",
        # 0b001_110: "",
        0b001_111: "SYNC",

        0b010_000: "MFHI",
        0b010_001: "MTHI",
        0b010_010: "MFLO",
        0b010_011: "MTLO",
        0b010_100: "DSLLV",
        # 0b010_101: "",
        0b010_110: "DSRLV",
        0b010_111: "DSRAV",

        0b011_000: "MULT",
        0b011_001: "MULTU",
        0b011_010: "DIV",
        0b011_011: "DIVU",
        0b011_100: "DMULT",
        0b011_101: "DMULTU",
        0b011_110: "DDIV",
        0b011_111: "DDIVU",

        0b100_000: "ADD",
        0b100_001: "ADDU",
        0b100_010: "SUB", # Subtract word
        0b100_011: "SUBU", # Subtract Unsigned word
        0b100_100: "AND",
        0b100_101: "OR",
        0b100_110: "XOR", # eXclusive OR
        0b100_111: "NOR",

        # 0b101_000: "",
        # 0b101_001: "",
        0b101_010: "SLT", # Set on Less Than
        0b101_011: "SLTU", # Set on Less Than Unsigned
        0b101_100: "DADD",
        0b101_101: "DADDU",
        0b101_110: "DSUB",
        0b101_111: "DSUBU",

        0b110_000: "TGE",
        0b110_001: "TGEU",
        0b110_010: "TLT",
        0b110_011: "TLTU",
        0b110_100: "TEQ",
        # 0b110_101: "",
        0b110_110: "TNE",
        # 0b110_111: "",

        0b111_000: "DSLL",
        # 0b111_001: "",
        0b111_010: "DSRL",
        0b111_011: "DSRA",
        0b111_100: "DSLL32",
        # 0b111_101: "",
        0b111_110: "DSRL32",
        0b111_111: "DSRA32",
    }

    def isJType(self) -> bool: # OP LABEL
        return False
    def isRType(self) -> bool: # OP rd, rs, rt
        return True # Not for all cases, but good enough
    def isIType(self) -> bool: # OP rt, IMM(rs)
        return False
    def isIType2(self) -> bool: # OP  rs, rt, IMM
        return False

    def getOpcodeName(self) -> str:
        opcode = "0x" + hex(self.function).strip("0x").zfill(2)
        return InstructionSpecial.SpecialOpcodes.get(self.rt, f"SPECIAL({opcode})")

class InstructionRegimm(Instruction):
    RegimmOpcodes = {
        0b00_000: "BLTZ",
        0b00_001: "BGEZ",
        0b00_010: "BLTZL",
        0b00_011: "BGEZL",

        0b01_000: "TGEI",
        0b01_001: "TGEIU",
        0b01_010: "TLTI",
        0b01_011: "TLTIU",

        0b10_000: "BLTZAL",
        0b10_001: "BGEZAL",
        0b10_010: "BLTZALL",
        0b10_011: "BGEZALL",

        0b01_100: "TEQI",
        0b01_110: "TNEI",
    }

    def isJType(self) -> bool: # OP LABEL
        return False
    def isRType(self) -> bool: # OP rd, rs, rt
        return False
    def isIType(self) -> bool: # OP rt, IMM(rs)
        return False
    def isIType2(self) -> bool: # OP  rs, rt, IMM
        return False

    def getOpcodeName(self) -> str:
        opcode = "0x" + hex(self.rt).strip("0x").zfill(2)
        return InstructionRegimm.RegimmOpcodes.get(self.rt, f"REGIMM({opcode})")

    def __str__(self) -> str:
        opcode = self.getOpcodeName().lower().ljust(7, ' ')
        rs = self.getRegisterName(self.rs)
        immediate = "0x" + hex(self.immediate).strip("0x").zfill(4).upper()

        result = f"{opcode} {rs},"
        result = result.ljust(14, ' ')
        return f"{result} {immediate}"


def wordToInstruction(word: int) -> Instruction:
    if ((word >> 26) & 0xFF) == 0x00:
        return InstructionSpecial(word)
    if ((word >> 26) & 0xFF) == 0x01:
        return InstructionRegimm(word)
    return Instruction(word)


class Text(File):
    def __init__(self, array_of_bytes):
        super().__init__(array_of_bytes)

        self.instructions: List[Instruction] = list()
        for word in self.words:
            self.instructions.append(wordToInstruction(word))

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
            instr1 = self.instructions[i]
            instr2 = other.instructions[i]
            if instr1.sameOpcodeButDifferentArguments(instr2):
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
            if args.ignore_branches:
                if instr1.isBranch() and instr2.isBranch() and instr1.sameOpcode(instr2):
                    instr1.blankOut()
                    instr2.blankOut()
                    was_updated = True

            #if (instr1.isADDIU() or instr1.isSB() or instr1.isSW() or instr1.isLWCz() 
            #    or instr1.isLBU() or instr1.isLH() or instr1.isLW() or instr1.isSWCz() 
            #    or instr1.isLHU() or instr1.isSH() or instr1.isLB() or instr1.isLUI()
            #    or instr1.isLDCz()):
            #    if instr1.sameOpcode(instr2) and instr1.sameBaseRegister(instr2) and instr1.rt == instr2.rt:
            #        if abs(instr1.immediate - instr2.immediate) == 0x10:
            #            instr1.blankOut()
            #            instr2.blankOut()

            opcode = instr1.getOpcodeName()

            if instr1.sameOpcode(instr2):
                if not lui_found:
                    if opcode == "LUI":
                        lui_found = True
                        lui_pos = i
                        lui_1_register = instr1.rt
                        lui_2_register = instr2.rt
                else:
                    if opcode == "ADDIU":
                        if instr1.rs == lui_1_register and instr2.rs == lui_2_register:
                            instr1.blankOut()
                            instr2.blankOut()
                            self.instructions[lui_pos].blankOut() # lui
                            other_file.instructions[lui_pos].blankOut() # lui
                            lui_found = False
                            was_updated = True
                    elif opcode == "LW":
                        if instr1.rs == lui_1_register and instr2.rs == lui_2_register:
                            instr1.blankOut()
                            instr2.blankOut()
                            self.instructions[lui_pos].blankOut() # lui
                            other_file.instructions[lui_pos].blankOut() # lui
                            lui_found = False
                            was_updated = True
                    elif opcode == "LWC1" or opcode == "LWC2":
                        if instr1.rs == lui_1_register and instr2.rs == lui_2_register:
                            instr1.blankOut()
                            instr2.blankOut()
                            self.instructions[lui_pos].blankOut() # lui
                            other_file.instructions[lui_pos].blankOut() # lui
                            lui_found = False
                            was_updated = True
                    elif opcode == "ORI":
                        if instr1.rs == lui_1_register and instr2.rs == lui_2_register:
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

    def removePointers(self):
        super().removePointers()

        lui_found = False
        lui_pos = 0
        lui_register = 0

        was_updated = False
        for i in range(len(self.instructions)):
            instr = self.instructions[i]
            opcode = instr.getOpcodeName()

            if not lui_found:
                if opcode == "LUI":
                    #immediate_half = ((instr.immediate >> 8) & 0xFF)
                    #if immediate_half == 0x80 or ((immediate_half & 0xF0) == 0 and (immediate_half & 0x0F) != 0):
                        #instr.blankOut()
                        #was_updated = True

                    lui_found = True
                    lui_pos = i
                    lui_register = instr.rt
            else:
                if opcode == "ADDIU" or opcode == "LW" or opcode == "LWC1" or opcode == "LWC2" or opcode == "ORI" or opcode == "LW":
                    if instr.rs == lui_register:
                        instr.blankOut()
                        self.instructions[lui_pos].blankOut() # lui
                        lui_found = False
                        was_updated = True

            if i > lui_pos + 5:
                lui_found = False

        if was_updated:
            self.updateWords()

    def updateWords(self):
        self.words = []
        for instr in self.instructions:
            self.words.append(instr.instr)
        self.updateBytes()

    def saveToFile(self, filepath: str):
        super().saveToFile(filepath + ".text")

        with open(filepath + ".text.asm", "w") as f:
            for instr in self.instructions:
                f.write(str(instr) + "\n")


class Data(File):
    def removePointers(self):
        super().removePointers()

        was_updated = False
        for i in range(self.sizew):
            top_byte = (self.words[i] >> 24) & 0xFF
            if top_byte == 0x80:
                self.words[i] = top_byte << 24
                was_updated = True
            if (top_byte & 0xF0) == 0x00 and (top_byte & 0x0F) != 0x00:
                self.words[i] = top_byte << 24
                was_updated = True
        
        if was_updated:
            self.updateBytes() 

    def saveToFile(self, filepath: str):
        super().saveToFile(filepath + ".data")


class Rodata(File):
    def saveToFile(self, filepath: str):
        super().saveToFile(filepath + ".rodata")


class Bss(File):
    def saveToFile(self, filepath: str):
        super().saveToFile(filepath + ".bss")


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

    def saveToFile(self, filepath: str):
        super().saveToFile(filepath + ".reloc")

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
        self.data = Data(self.bytes[start:end])

        start += data_size
        end += rodata_size
        self.rodata = Rodata(self.bytes[start:end])

        start += rodata_size
        end += bss_size
        self.bss = Bss(self.bytes[start:end])

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

    def removePointers(self):
        super().removePointers()

        self.text.removePointers()
        self.data.removePointers()
        self.rodata.removePointers()
        self.bss.removePointers()
        self.reloc.removePointers()

        self.updateBytes()

    def updateBytes(self):
        self.words = self.text.words + self.data.words + self.rodata.words + self.bss.words + self.header + self.reloc.words + self.tail
        super().updateBytes()

    def saveToFile(self, filepath: str):
        self.text.saveToFile(filepath)
        self.data.saveToFile(filepath)
        self.rodata.saveToFile(filepath)
        self.bss.saveToFile(filepath)
        self.reloc.saveToFile(filepath)



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

def removePointers(args, filedata: bytearray) -> bytearray:
    if not args.ignore04: # This will probably grow...
        return filedata
    
    words = bytesToBEWords(filedata)
    for i in range(len(words)):
        w = words[i]
        if args.ignore04:
            if ((w >> 24) & 0xFF) == 0x04:
                words[i] = 0x04000000
    return beWordsToBytes(words, filedata)


def getHashesOfFiles(args, filesPath: List[str]) -> List[str]:
    hashList = []
    for path in filesPath:
        f = readFileAsBytearray(path)
        if len(f) != 0:
            fHash = getStrHash(removePointers(args, f))
            line = fHash + " " + path # To be consistent with runCommandGetOutput("md5sum", md5arglist)
            hashList.append(line)
    return hashList

def compareFileAcrossVersions(args, versionsList: List[str], filename: str) -> List[str]:
    md5arglist = list(map(lambda orig_string: "baserom_" + orig_string + "/" + filename, versionsList))
    # os.system( "md5sum " + " ".join(filesPath) )

    # Get hashes.
    # output = runCommandGetOutput("md5sum", filesPath)
    output = getHashesOfFiles(args, md5arglist)

    # Print md5hash
    #print("\n".join(output))
    #print()

    filesHashes = dict() # "NN0": "339614255f179a1e308d954d8f7ffc0a"
    firstFilePerHash = dict() # "339614255f179a1e308d954d8f7ffc0a": "NN0"

    for line in output:
        trimmed = removeExtraWhitespace(line)
        filehash, filepath = trimmed.split(" ")
        abbr = getVersionAbbr(filepath)

        # Map each abbreviation and its hash.
        filesHashes[abbr] = filehash

        # Find out where in which version this hash appeared for first time.
        if filehash not in firstFilePerHash:
            firstFilePerHash[filehash] = abbr

    row = []
    for ver in versionsList:
        abbr = versions.get(ver, None)

        if abbr in filesHashes:
            fHash = filesHashes[abbr]
            row.append(firstFilePerHash[fHash])
        else:
            row.append("")
    return row

def compareOverlayAcrossVersions(args, versionsList: List[str], filename: str) -> List[List[str]]:
    column = []

    if filename.startswith("ovl_"):
        filesHashes = dict() # "filename": {"NN0": hash}
        firstFilePerHash = dict() # "filename": {hash: "NN0"}

        for version in versionsList:
            path = "baserom_" + version + "/" + filename

            array_of_bytes = readFileAsBytearray(path)
            if len(array_of_bytes) == 0:
                continue

            f = Overlay(array_of_bytes)
            f.removePointers()
            if args.savetofile:
                new_file_path = os.path.join(args.savetofile, version + "_" + filename)
                f.saveToFile(new_file_path)

            abbr = getVersionAbbr(path)

            if filename + ".text" not in filesHashes:
                filesHashes[filename + ".text"] = dict()
                firstFilePerHash[filename + ".text"] = dict()
            if filename + ".data" not in filesHashes:
                filesHashes[filename + ".data"] = dict()
                firstFilePerHash[filename + ".data"] = dict()
            if filename + ".rodata" not in filesHashes:
                filesHashes[filename + ".rodata"] = dict()
                firstFilePerHash[filename + ".rodata"] = dict()
            if filename + ".bss" not in filesHashes:
                filesHashes[filename + ".bss"] = dict()
                firstFilePerHash[filename + ".bss"] = dict()
            if filename + ".reloc" not in filesHashes:
                filesHashes[filename + ".reloc"] = dict()
                firstFilePerHash[filename + ".reloc"] = dict()

            textHash = f.text.getHash()
            dataHash = f.data.getHash()
            rodataHash = f.rodata.getHash()
            bssHash = f.bss.getHash()
            relocHash = f.reloc.getHash()

            # Map each abbreviation to its hash.
            filesHashes[filename + ".text"][abbr] = textHash
            filesHashes[filename + ".data"][abbr] = dataHash
            filesHashes[filename + ".rodata"][abbr] = rodataHash
            filesHashes[filename + ".bss"][abbr] = bssHash
            filesHashes[filename + ".reloc"][abbr] = relocHash

            # Find out where in which version this hash appeared for first time.
            if textHash not in firstFilePerHash[filename + ".text"]:
                firstFilePerHash[filename + ".text"][textHash] = abbr
            if dataHash not in firstFilePerHash[filename + ".data"]:
                firstFilePerHash[filename + ".data"][dataHash] = abbr
            if rodataHash not in firstFilePerHash[filename + ".rodata"]:
                firstFilePerHash[filename + ".rodata"][rodataHash] = abbr
            if bssHash not in firstFilePerHash[filename + ".bss"]:
                firstFilePerHash[filename + ".bss"][bssHash] = abbr
            if relocHash not in firstFilePerHash[filename + ".reloc"]:
                firstFilePerHash[filename + ".reloc"][relocHash] = abbr

        for section in [".text", ".data", ".rodata", ".bss", ".reloc"]:
            row = [filename + section]
            for version in versionsList:
                abbr = versions[version]

                if abbr in filesHashes[filename + section]:
                    fHash = filesHashes[filename + section][abbr]
                    row.append(firstFilePerHash[filename + section][fHash])
                else:
                    row.append("")
            column.append(row)
    else:
        filesHashes = dict() # "NN0": "339614255f179a1e308d954d8f7ffc0a"
        firstFilePerHash = dict() # "339614255f179a1e308d954d8f7ffc0a": "NN0"

        for version in versionsList:
            path = "baserom_" + version + "/" + filename

            array_of_bytes = readFileAsBytearray(path)
            if len(array_of_bytes) == 0:
                continue

            f = File(array_of_bytes)
            f.removePointers()
            if args.savetofile:
                new_file_path = os.path.join(args.savetofile, version + "_" + filename)
                f.saveToFile(new_file_path)

            abbr = getVersionAbbr(path)
            filehash = f.getHash()

            # Map each abbreviation to its hash.
            filesHashes[abbr] = filehash

            # Find out where in which version this hash appeared for first time.
            if filehash not in firstFilePerHash:
                firstFilePerHash[filehash] = abbr

        row = [filename]
        for version in versionsList:
            abbr = versions[version]

            if abbr in filesHashes:
                fHash = filesHashes[abbr]
                row.append(firstFilePerHash[fHash])
            else:
                row.append("")
        column.append(row)
    return column


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("versionlist", help="Path to version list.")
    parser.add_argument("filelist", help="List of filenames of the ROM that will be compared.")
    parser.add_argument("--noheader", help="Disables the csv header.", action="store_true")
    parser.add_argument("--ignore04", help="Ignores words starting with 0x04.", action="store_true")
    parser.add_argument("--overlays", help="Treats the files in filelist as overlays.", action="store_true")
    parser.add_argument("--savetofile", help="Specify a folder where each part of an overlay will be written. The folder must already exits.", metavar="FOLDER")
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
        if args.overlays:
            column = compareOverlayAcrossVersions(args, lines, filename)

            for row in column:
                # Print csv row
                for cell in row:
                    print(cell + ",", end="")
                print(countUnique(row)-1, end="")
                print()

        else:
            row = compareFileAcrossVersions(args, lines, filename)

            # Print csv row
            print(filename, end="")
            for cell in row:
                print("," + cell, end="")
            print("," + str(countUnique(row)), end="")
            print()

if __name__ == "__main__":
    main()
