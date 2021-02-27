#!/usr/bin/python3

import os
import re
import argparse

script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = script_dir + "/.."
if not script_dir.endswith("/tools"):
    root_dir = script_dir
src_actors_dir = root_dir + "/src/overlays/actors"
src_code_dir = root_dir + "/src/code"
actors_in_code = {
    "oot": ["z_en_a_keep.c", "z_en_item00.c", "z_player_call.c"],
    "mm": []
}
actors_enum_file = {
    "oot": "include/z64actor.h",
    "mm": "include/z64actor.h",
}
objects_enum_file = {
    "oot": "include/z64object.h",
    "mm": "include/z64object.h",
}
initvars_pattern = re.compile(r"const ActorInit (?P<actor_name>[\w]+)_InitVars = \{(?P<initvars>(\s*[\w\(\)],*\s*)+)\};")
enum_entry_pattern = re.compile(r"\/\*\s*(?P<hex>0x[0-9a-fA-F]+)\s*\*\/\s*(?P<name>\w+)")
actors_enum_pattern = re.compile(r"typedef enum \{\s*(?P<ids>[^\{\}]+)\s*\} ActorID;")
objects_enum_pattern = re.compile(r"typedef enum \{\s*(?P<ids>[^\{\}]+)\s*\} ObjectID;")


def find_initvars_in_file(filepath):
    with open(filepath) as f:
        f_contents = f.read()
    initvars_match = initvars_pattern.search(f_contents)
    if initvars_match is not None:
        actor_name = initvars_match.group("actor_name")
        initvars = initvars_match.group("initvars")
        initvars = initvars.strip().split(",")
        vars_data = []
        for var in initvars:
            if var:
                vars_data.append(var.strip())
        return (actor_name, vars_data)

    return (None, None)

def get_ids_from_enum(filepath, enum_regex):
    actors_id = {}

    with open(filepath) as f:
        f_contents = f.read()
    match = enum_regex.search(f_contents)
    if match is not None:
        ids = match.group("ids")
        for entry in enum_entry_pattern.finditer(ids):
            hex_id = entry.group("hex")
            name = entry.group("name")
            actors_id[name] = hex_id

    return actors_id


def get_actors_id(mode):
    return get_ids_from_enum(root_dir + "/" + actors_enum_file[mode], actors_enum_pattern)

def get_objects_id(mode):
    return get_ids_from_enum(root_dir + "/" + objects_enum_file[mode], objects_enum_pattern)


def get_every_initvars(mode):
    actors = {}

    for actor_folder in os.listdir(src_actors_dir):
        initvars_found = False
        actor_path = src_actors_dir + "/" + actor_folder
        for filename in os.listdir(actor_path):
            actor_name, actor_data = find_initvars_in_file(actor_path + "/" + filename)
            if actor_name is not None:
                actors[actor_name] = actor_data
                initvars_found = True
        if not initvars_found:
            #print(actor_path)
            pass

    if mode is not None:
        for filename in actors_in_code[mode]:
            actor_name, actor_data = find_initvars_in_file(src_code_dir + "/" + filename)
            if actor_name is not None:
                actors[actor_name] = actor_data

    return actors


def get_list_from_file(filename):
    actor_list = []
    if filename is not None:
        with open(filename) as f:
            actor_list = list(map(lambda x: x.strip().split(",")[0], f.readlines()))
    return actor_list


def print_list_as_csv(lis):
    for value in lis:
        print(",".join(value))


def main():
    #description = "Collects actor's functions sizes, and print them in csv format."
    description = "Parse actor's InitVars to get the main object of each actor. The output is printed in csv format."

    #epilog = """\
#To make a .csv with the data, simply redirect the output. For example:
#    ./tools/get_actor_sizes.py > results.csv

#Flags can be mixed to produce a customized result:
#    ./tools/get_actor_sizes.py --function-lines --non-matching > status.csv
#    ./tools/get_actor_sizes.py --non-matching --ignore pull_request.csv > non_matching.csv
#    ./tools/get_actor_sizes.py --non-matching --function-lines --include-only my_reserved.csv > my_status.csv
#    """
    epilog = "epilog"
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--mode", help="", choices=["oot", "mm"], default="oot")
    args = parser.parse_args()

    #objs = find_objects_in_actors(args.mode)
    actors_ids = get_actors_id(args.mode)
    objects_ids = get_objects_id(args.mode)
    actors_vars = get_every_initvars(args.mode)

    result = []
    ids_found = set()

    for actor_name, actor_vars in actors_vars.items():
        actor_id = actor_vars[0]
        object_id = actor_vars[3]

        actor_id_hex = actors_ids.get(actor_id, actor_id)
        object_id_hex = objects_ids.get(object_id, object_id)

        result.append([actor_id_hex, actor_id, actor_name, object_id_hex, object_id])
        ids_found.add(actor_id)

    for id_name, id_hex in actors_ids.items():
        if id_name not in ids_found:
            result.append([id_hex, id_name, "", "", ""])
    
    header = ["Actor id", "Actor name", "Overlay name", "Object id", "Object name"]
    print(",".join(header))

    result.sort()
    print_list_as_csv(result)


if __name__ == "__main__":
    main()
