#!/usr/bin/python3


import argparse
import json
import pprint


ELEMENTS_SEP=' '


class Preprocesser:
    def __init__(self, funcs):
        self.function_set = dict()
        for func in funcs:
            self.function_set[func.__name__] = func


def preprocess_field(json_obj, field, preprocesser):
    elements = field.split(ELEMENTS_SEP)
    for i, e in enumerate(elements):
        if e[0] == '!':
            func = preprocesser.function_set[e[1:]]
            suffix = elements[i:]
            suffix = func(json_obj, suffix)
            new_field = ""
            if i != 0:
                new_field = new_field + ELEMENTS_SEP.join(elements[:i]) + ELEMENTS_SEP
            new_field = new_field + suffix
            return preprocess_field(json_obj, new_field, preprocesser)
    return field


def preprocess(current_sub_tree, json_obj, preprocesser):
    for key, value in current_sub_tree.items():
        if isinstance(value, dict):
            preprocess(value, json_obj, preprocesser)
        else:
            current_sub_tree[key] = preprocess_field(json_obj, value, preprocesser)



def var(json_obj, suffix):
    key = suffix[1]
    result_str = json_obj['var'][key]
    if len(suffix) > 2:
        result_str = result_str + ELEMENTS_SEP + ELEMENTS_SEP.join(suffix[2:])
    return result_str

def seq(json_obj, suffix):
    sequence = list(range(int(suffix[1]), int(suffix[3]) + 1, int(suffix[2])))
    result_str = ELEMENTS_SEP.join(map(str, sequence))
    if len(suffix) > 4:
        result_str = result_str + ELEMENTS_SEP + ELEMENTS_SEP.join(suffix[4:])
    return result_str

def exp_seq(json_obj, suffix):
    base = int(suffix[1])
    q = float(suffix[2])
    lim = int(suffix[3]) + 1
    sequence = []
    n = 0
    item = 0
    while (item := int(base * q ** n)) < lim:
        sequence.append(item)
        n += 1

    result_str = ELEMENTS_SEP.join(map(str, sequence))
    if len(suffix) > 4:
        result_str = result_str + ELEMENTS_SEP + ELEMENTS_SEP.join(suffix[4:])
    return result_str


def main():
    parser = argparse.ArgumentParser(
        prog='JSON preprocesser',
        description='Dont fucking know why have i done that')
    parser.add_argument('-i', '--input-file', nargs='?', default='config.json')
    parser.add_argument('-o', '--output-file', nargs='?')
    parser.add_argument('--indent', nargs='?', type=int, default=4)

    args = parser.parse_args()

    preprocesser = Preprocesser([var, seq, exp_seq])

    with open(args.input_file, "r") as f:
        configuration = json.load(f)

    section_name = 'var'
    preprocess(configuration[section_name], configuration, preprocesser)
    section_name = 'realizations'
    preprocess(configuration[section_name], configuration, preprocesser)

    if args.output_file:
        with open(args.output_file, "w") as f:
            json.dump(configuration, f, indent=args.indent)
    else:
        print(json.dumps(configuration, indent=args.indent))


if __name__ == '__main__':
    main()
