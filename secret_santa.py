import random
import os
import shutil
from typing import Tuple, List
from validate import validate

__DEFAULT_OUTPUT_FOLDER__ = 'output'

def create_output_folder(output_folder:str=__DEFAULT_OUTPUT_FOLDER__) -> None:
    # If the output folder already exists, delete it and create a new one.
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

def get_random_locs() -> Tuple[int]:
    loc1 = random.choice([0,1])
    loc2 = 1 if loc1 == 0 else 0
    return loc1, loc2

def create_groups(participants:list) -> List[list]:
    """
    Splits the participants randomly into two groups. This prevents spouses from being assigned to
    each other.
    """
    # If all participants are single, return as a single group
    if sum([isinstance(p, str) for p in participants]) == len(participants):
        return [participants]
    # If the participants contain couples, do the random split
    groups = [[],[]]
    for p in participants:
        if isinstance(p, str):
            loc, _ = get_random_locs()
            groups[loc].append(p)
        else:
            loc1, loc2 = get_random_locs()
            groups[loc1].append(p[0])
            groups[loc2].append(p[1])
    return groups

def get_eligible_names(name_list:list, participant:str, already_picked:dict, reciprocity:bool=False) -> list:
    """
    Returns a list of eligible names that the participant can be assigned to.
    If reciprocity is True, two people can be assigned to each other. If False, they cannot. The default
    is False because, with odd-numbered groups, it is possible that not everyone can be assigned a person
    if reciprocity=True.
    """
    ineligible_names = [participant] + list(already_picked.keys())
    if not reciprocity:
        ineligible_names.append(already_picked.get(participant, ""))
    return [name for name in name_list if name not in ineligible_names]

def assign_one_name(participant:str, eligible_names:List[str], output_folder:str) -> str:
    """
    Takes a name, and their assigned name, and writes the name to the output file.
    Returns the assigned name.
    """
    assigned_name = random.choice(eligible_names)
    with open(f"{output_folder}/{participant}.txt", "w") as outfile:
        outfile.write(assigned_name)
    return assigned_name

def assign_names(group:List[str], output_folder:str=__DEFAULT_OUTPUT_FOLDER__) -> None:
    """
    Takes a list of participants, assigns them a name, and writes each assigned name to a .txt file.
    """
    random.shuffle(group)
    already_picked = {}
    for name in group:
        assigned_name = assign_one_name(
            participant=name,
            eligible_names=get_eligible_names(group, name, already_picked),
            output_folder=output_folder
        )
        already_picked[assigned_name] = name

def run(participants, output_folder:str=__DEFAULT_OUTPUT_FOLDER__) -> None:
    create_output_folder(output_folder)
    groups = create_groups(participants)
    for group in groups:
        assign_names(group, output_folder)
    validate(participants, output_folder)
    print(f"Picks complete. See {output_folder}/*.txt")

if __name__ == "__main__":
    participants = [
        ["Greg", "Megan"],
        ["Russell", "Sondra"],
        ["Josh", "Caitlin"],
    ]
    run(participants)
