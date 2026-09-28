from BKT import BKT
import helper


N = 10

# cd to classicalBKT
init_state = helper.read_initial_state("test/test_state.json")
skill_names = helper.get_skill_names(init_state)
questions = helper.read_jsonl("test/test_data.jsonl")

bkt = BKT(
    skill_names=skill_names,
    prior=0.10,learn=0.20,guess=0.20,slip=0.10
)

current_state = init_state

for count in range(N):
    question_data = helper.choose(questions, current_state)

    print(f"Question {count + 1}: {question_data['question']}")
    response = input("Your answer: ").strip()

    correctness = (
        response.lower()
        == question_data["answer"].strip().lower()
    )

    current_state = bkt.Update(
        previous_state=current_state,
        data=question_data,
        correctness=correctness
    )

    print("Correct:", correctness)
    print("Current state:", current_state)
    print()

print("Final state:", current_state)