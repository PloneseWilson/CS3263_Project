import json

def read_jsonl(path):
    questions = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                questions.append(json.loads(line))

    return questions

def read_initial_state(path):
    with open(path, "r", encoding="utf-8") as file:
        state_data = json.load(file)

    return state_data["skill"]

def get_skill_names(initial_state):
    return list(initial_state.keys())

