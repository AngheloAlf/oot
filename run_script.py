import argparse
import os
from multiprocessing import Pool, cpu_count

def readFile(filepath):
    with open(filepath) as f:
        return f.readlines()

def runScript(script, line):
    command = f"python {script} {line}"
    print(command)
    
    return os.system(command)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="Path to python script.")
    parser.add_argument("filepath", help="Path to file.")
    args = parser.parse_args()

    lines = readFile(args.filepath)

    numCores = cpu_count()
    print(f"Using {numCores} CPU cores.")

    p = Pool(numCores)
    p.map(lambda x: runScript(args.script, x), lines)

    #for line in lines:
    #    runScript(args.script, line)


if __name__ == "__main__":
    main()
