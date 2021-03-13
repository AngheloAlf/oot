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
        zz = self.opcode & 0x03
        if zz == 0x00 or zz == 0x03:
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

    def isBranch(self) -> bool:
        return (self.isBEQ() or self.isBEQL() or self.isBLEZ() or self.isBLEZL() 
                or self.isBGTZ() or self.isBGTZL() or self.isBNE() or self.isBNEL() 
                or self.isJ() or self.isJAL())

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
        return self.opcode == (0x9C >> 2) # 0b100111

    def isPREF(self) -> bool: # Prefetch
        return self.opcode == (0xCC >> 2) # 0b110011

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

    def isCOPz(self) -> bool: # Coprocessor OPeration
        #if (self.opcode & 0x03) == 0x00:
        #    return False
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
        zz = self.opcode & 0x03
        if zz == 0x00 or zz == 0x03:
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

    def getOpcodeName(self) -> str:
        # TODO: 0x10 (COP0), 
        if self.isLUI():
            return "LUI"
        elif self.isADDIU():
            return "ADDIU"
        elif self.isLW():
            return "LW"
        elif self.isLWCz():
            return f"LWC{self.opcode&0x03}"
        elif self.isANDI():
            return "ANDI"
        elif self.isORI():
            return "ORI"
        elif self.isADDI():
            return "ADDI"
        elif self.isDADDI():
            return "DADDI"
        elif self.isDADDIU():
            return "DADDIU"

        elif self.isBEQ():
            return "BEQ"
        elif self.isBEQL():
            return "BEQL"
        elif self.isBLEZ():
            return "BLEZ"
        elif self.isBLEZL():
            return "BLEZL"
        elif self.isBGTZ():
            return "BGTZ"
        elif self.isBGTZL():
            return "BGTZL"
        elif self.isBNE():
            return "BNE"
        elif self.isBNEL():
            return "BNEL"

        elif self.isJ():
            return "J"
        elif self.isJAL():
            return "JAL"

        elif self.isLB():
            return "LB"
        elif self.isLBU():
            return "LBU"

        elif self.isLD():
            return "LD"

        elif self.isLDCz():
            return f"LDC{self.opcode&0x3}"

        elif self.isLDL():
            return "LDL"
        elif self.isLDR():
            return "LDR"

        elif self.isLH():
            return "LH"
        elif self.isLHU():
            return "LHU"

        elif self.isLL():
            return "LL"
        elif self.isLLD():
            return "LLD"

        elif self.isLWL():
            return "LWL"
        elif self.isLWR():
            return "LWR"

        elif self.isLWU():
            return "LWU"

        elif self.isPREF():
            return "PREF"

        elif self.isSB():
            return "SB"
        elif self.isSC():
            return "SC"
        elif self.isSCD():
            return "SCD"
        elif self.isSD():
            return "SD"

        elif self.isSDCz():
            return f"SDC{self.opcode&0x03}"

        elif self.isSDL():
            return "SDL"
        elif self.isSDR():
            return "SDR"

        elif self.isCOPz():
            zz = self.opcode&0x03
            if zz == 0x03:
                return "COP1X"
            return f"COP{zz}"

        elif self.isSH():
            return "SH"

        # SLL # Shift word Left Logical
        # SLLV # Shift word Left Logical Variable
        # SLT # Set on Less Than

        elif self.isSLTI():
            return "SLTI"
        elif self.isSLTIU():
            return "SLTIU"

        # SLTU # Set on Less Than Unsigned

        # SRA # Shift word Right Arithmetic
        # SRAV # Shift word Right Arithmetic Variable
        # SRL # Shift word Right Logical
        # SRLV # Shift word Right Logical Variable

        # SUB # Subtract word
        # SUBU # Subtract Unsigned word

        elif self.isSW():
            return "SW"
        elif self.isSWCz():
            return f"SWC{self.opcode&0x03}"

        elif self.isSWL():
            return "SWL"
        elif self.isSWR():
            return "SWR"

        # XOR # eXclusive OR

        elif self.isXORI():
            return "XORI"

        elif self.isCOPz():
            return f"COP{self.opcode&0x3}"

        elif self.isSPECIAL():
            return "SPECIAL"
        elif self.isREGIMM():
            return "REGIMM"

        opcode = hex(self.opcode)
        eprint(f"Unknown opcode: {opcode}")
        return opcode

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
        elif 32 <= register <= 63:
            return "$f" + str(register-32)

        eprint(f"Unknown register: {register}")
        return hex(register)

    def __str__(self) -> str:
        opcode = self.getOpcodeName().lower().ljust(8, ' ')
        baseRegister = (self.getRegisterName(self.baseRegister) + ",").ljust(6, ' ')
        rt = (self.getRegisterName(self.rt) + ",").ljust(6, ' ')
        immediate = "0x" + hex(self.immediate).strip("0x").zfill(4)
        return f"{opcode} {baseRegister} {rt} {immediate}"

    def __repr__(self) -> str:
        return self.__str__()

class InstructionSpecial(Instruction):
    pass

class InstructionRegimm(Instruction):
    pass

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
                elif instr1.isLWCz() and instr2.isLWCz():
                    if instr1.baseRegister == lui_1_register and instr2.baseRegister == lui_2_register:
                        instr1.blankOut()
                        instr2.blankOut()
                        self.instructions[lui_pos].blankOut() # lui
                        other_file.instructions[lui_pos].blankOut() # lui
                        lui_found = False
                        was_updated = True
                elif instr1.isORI() and instr2.isORI():
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

    def removePointers(self):
        super().removePointers()

        lui_found = False
        lui_pos = 0
        lui_register = 0

        was_updated = False
        for i in range(len(self.instructions)):
            instr = self.instructions[i]
            if not lui_found:
                if instr.isLUI():
                    immediate_half = ((instr.immediate >> 8) & 0xFF)
                    if immediate_half == 0x80 or ((immediate_half & 0xF0) == 0 and (immediate_half & 0x0F) != 0):
                        #instr.blankOut()
                        #was_updated = True

                        lui_found = True
                        lui_pos = i
                        lui_register = instr.rt
            else:
                if instr.isADDIU() or instr.isLW() or instr.isLWCz() or instr.isORI() or instr.isLW():
                    if instr.baseRegister == lui_register:
                        instr.blankOut()
                        self.instructions[lui_pos].blankOut() # lui
                        lui_found = False
                        was_updated = True

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

def compareOverlayAcrossVersions(args, versionsList: List[str], filename: str) -> List[str]:
    filesHashes = dict() # "NN0": "339614255f179a1e308d954d8f7ffc0a"
    firstFilePerHash = dict() # "339614255f179a1e308d954d8f7ffc0a": "NN0"

    #for path in md5arglist:
    for version in versionsList:
        path = "baserom_" + version + "/" + filename

        array_of_bytes = readFileAsBytearray(path)
        if len(array_of_bytes) > 0:
            if filename.startswith("ovl_"):
                f = Overlay(array_of_bytes)
            else:
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

    row = []
    for version in versionsList:
        abbr = versions[version]

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
            row = compareOverlayAcrossVersions(args, lines, filename)
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
