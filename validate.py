from typing import List
import os
import shutil
import string
import random
import json

def flatten_list(list_of_lists:List[list]) -> list:
    """ Converts a nested list to a flattened list. """
    out_list = []
    for i in list_of_lists:
        if isinstance(i, str):
            out_list.append(i)
        else:
            out_list += i
    return out_list

def get_picked_names(output_folder:str, output_files:List[str]) -> List[str]:
    picked_names = []
    for f in output_files:
        with open(f"{output_folder}/{f}", "r") as txt_file:
            picked_names.append(txt_file.read())
    return picked_names

def test_for_correct_number_of_files(output_files:List[str], participants:list) -> None:
    assert len(output_files) == len(flatten_list(participants)), f"{len(output_files)} output files and {len(participants)} participants"

def test_for_duplicate_output_files(output_files:List[str]) -> None:
    for f in output_files:
        if output_files.count(f) > 1:
            raise Exception(f"Output file {f} is duplicated.")

def test_for_duplicate_assignment(picked_names:List[str]) -> None:
    for name in picked_names:
        if picked_names.count(name) > 1:
            raise Exception(f"{name} picked {picked_names.count(name)} times.")

def test_every_participant_has_been_assigned(participants:list, picked_names:list) -> None:
    for name in flatten_list(participants):
        assert name in picked_names, f"{name} was not assigned"

def test_spouses_not_assigned_to_each_other(output_folder:str, participants:list) -> None:
    spouse_groups = [p for p in participants if isinstance(p, list)]
    for spouse_group in spouse_groups:
        for spouse in spouse_group:
            with open(f"{output_folder}/{spouse}.txt", "r") as f:
                assert f.read() not in spouse_group, f"{f.read()} picked by {spouse}."

def validate(participants:list, output_folder:str) -> None:
    """ Validates that the secret santa picks were done correctly. """
    output_files = [file for file in os.listdir(output_folder) if file.endswith(".txt")]
    picked_names = get_picked_names(output_folder, output_files)
    test_for_duplicate_output_files(output_files)
    test_for_duplicate_assignment(picked_names)
    test_every_participant_has_been_assigned(participants, picked_names)
    test_spouses_not_assigned_to_each_other(output_folder, participants)

def mock_participants() -> list:
    def random_string(characters=string.ascii_uppercase+string.ascii_lowercase):
        return ''.join([random.choice(characters) for _ in range(10)])
    participant_list_length = random.choice(range(2, 100))
    participants = []
    for i in range(0, participant_list_length):
        if random.choice(["string", "list"]) == "string":
            participants.append(random_string())
        else:
            participants.append([random_string(), random_string()])
    return participants

def stress_test():
    """ Runs the program 1000 times with mocked list names. """
    import secret_santa
    for i in range(0, 1000):
        participants = mock_participants()
        try:
            secret_santa.run(
                participants=participants,
                output_folder='stress_test'
            )
        except Exception as e:
            msg = f"Stress test failed with error:\n{e}\n\nParticipant list: {json.dumps(participants, indent=2)}"
            raise Exception(msg)
        finally:
            shutil.rmtree('stress_test')


if __name__ == "__main__":
    stress_test()
