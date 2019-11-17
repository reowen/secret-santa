import random
import os
import shutil
from typing import Tuple, List

__DEFAULT_OUTPUT_FOLDER__ = 'output'

def create_output_folder(output_folder:str=__DEFAULT_OUTPUT_FOLDER__) -> None:
    # If the output folder already exists, delete it and create a new one.
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

def exclude_already_picked(spouse_groups:list, exclude:list) -> list:
    """ Takes a list of spouses, and removes any people who were already picked. """
    for index, couple in enumerate(spouse_groups):
        spouse_groups[index] = [name for name in couple if name not in exclude]
    return spouse_groups

def write_pick(spouse:str, assigned_name:str, output_folder:str) -> str:
    """
    Takes a name, and their assigned name, and writes the name to the output file.
    Returns the assigned name.
    """
    with open(f"{output_folder}/{spouse}.txt", "w") as outfile:
        outfile.write(assigned_name)
    return assigned_name

def gen_picks(participants:List[str], output_folder:str=__DEFAULT_OUTPUT_FOLDER__) -> None:
    """
    Takes a list of participants, assigns them a name, and writes each assigned name to a .txt file.
    """
    random.shuffle(participants)
    already_picked = []
    for spouse_group in participants:
        other_couples = exclude_already_picked(
            spouse_groups=[couple for couple in participants if couple != spouse_group],
            exclude=already_picked,
        )
        # Randomly assign from other couples, ensuring that at least one person from each couple is assigned
        index_range = range(0, len(other_couples))
        loc1 = random.choice([i for i in index_range if len(other_couples[i]) > 0])
        loc2 = random.choice([i for i in index_range if len(other_couples[i]) > 0 and i != loc1])
        pick1 = write_pick(spouse_group[0], random.choice(other_couples[loc1]), output_folder)
        pick2 = write_pick(spouse_group[1], random.choice(other_couples[loc2]), output_folder)
        already_picked += [pick1, pick2]
    print(f"Picks complete. See {output_folder}/*.txt")

def flatten_list(list_of_lists:list) -> list:
    out_list = []
    for i in list_of_lists:
        out_list += i
    return out_list

def validate_picks(participants:list, output_folder:str=__DEFAULT_OUTPUT_FOLDER__) -> None:
    output_files = [file for file in os.listdir(output_folder) if file.endswith(".txt")]
    assert len(output_files) == len(flatten_list(participants)), f"{len(output_files)} output files and {len(participants)} participants"
    # Check for duplicate output files
    for f in output_files:
        if output_files.count(f) > 1:
            raise Exception(f"Output file {f} is duplicated.")
    # Validate that the same person was not assigned to two different people.
    picked_names = []
    for f in output_files:
        with open(f"{output_folder}/{f}", "r") as txt_file:
            picked_names.append(txt_file.read())
    for name in picked_names:
        if picked_names.count(name) > 1:
            raise Exception(f"{name} picked {picked_names.count(name)} times.")
    # Validate every participant has been assigned to someone
    for name in flatten_list(participants):
        assert name in picked_names, f"{name} was not assigned"
    # Validate that spouses did not pick each other
    for spouse_group in participants:
        for spouse in spouse_group:
            with open(f"{output_folder}/{spouse}.txt", "r") as f:
                assert f.read() not in spouse_group, f"{f.read()} picked by {spouse}."

if __name__ == "__main__":
    create_output_folder()
    participants = [
        ["Greg", "Megan"],
        ["Russell", "Sondra"],
        ["Josh", "Caitlin"],
    ]
    gen_picks(participants)
    validate_picks(participants)
