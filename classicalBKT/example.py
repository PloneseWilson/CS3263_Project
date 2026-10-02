from BKT import BKT
from skill import Skill
import helper
import skill

N = 10
TOPK = 5

# change the path to match your Root -> Data path
init_state = helper.read_initial_state("classicalBKT/test/test_state2.json")
skill_names = helper.get_skill_names(init_state)
questions = helper.read_jsonl("classicalBKT/test/test_data2.jsonl")

# BKT class
bkt = BKT(
    learn=0.20,guess=0.20,slip=0.10
)

# current state: learner's understanding on each topics
# skills: the list containing skill of each question, order preserved
current_state = init_state
skills = skill.build_Skill(skill_names, questions)

for count in range(N):
    index = skill.choose_index(current_state, skills, K = TOPK)  # choose next question
    question_data = questions[index]

    print(f"Question {count + 1}: {question_data['question']}") # interaction
    response = input("Your answer: ").strip()

    correctness = (
        response.lower()
        == question_data["answer"].strip().lower() # check correctness
    )

    current_state = bkt.Update( # update
        previous_state=current_state,
        data=question_data,
        correctness=correctness
    )

    print("Correctness:", correctness)
    print()

print("Final state:", current_state)