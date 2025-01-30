#!/usr/bin/python3


import sys
import subprocess


ELEMENTS_SEP=' '


def main():
    target_name = []
    files = []
    flags = []
    
    target_started = 0
    files_started = 0
    flags_started = 0
    for arg in sys.argv[1:]:
        if arg == '-o':
            target_started = 1
            files_started = 0
            flags_started = 0
            continue
        if arg == '-f':
            target_started = 0
            files_started = 1
            flags_started = 0
            continue
        if arg == '--options':
            target_started = 0
            files_started = 0
            flags_started = 1
            continue

        if target_started:
            target_name.append(arg)
        if files_started:
            files.append(arg)
        if flags_started:
            flags.append(arg)

    target_name_str = " ".join(target_name)
    files_str = " ".join([file if file[-2:] == '.c' else "" for file in files])
    flags_str = " ".join(flags)
    
    program = subprocess.Popen(["make", "--makefile=c_makefile", f"TARGET={target_name_str}", f"SRCS={files_str}", f"SPECIFIC_FLAGS={flags_str}"])
    output, error = program.communicate()

    return error


if __name__ == '__main__':
    main()
