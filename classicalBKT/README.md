# Require Python 3.10+

## Templates
Check template/  
1. **state_template**: the init state of learners, represent their initial capability of each topics. Values should fall in [0,1]
2. **data_template**: the jsonl input's each line of data, and the skill required are equally weighed
3. **data_template_with_label_weight**: same as above, but skills have weights, which will be normalized by L2.

## Execution
- place files into test/
    - state must match any state_templates
    - questions must be a jsonl containing any of the same data_templates each line
- edit the path of init_state and questions in **example.py**

## Selection Algorithm
- Compare the **cosine similarity** of current learning state and each question's skill vector
- Choose the one with least cosine similarity to check user's knowledge in topics with poor performance
- Use the **top-K** design(actually bottom K) here to add randomness in the question selected

## Toggle
- **DEBUG** in selection algorithm: environment variables in skill.py, print top K choice and their similarities
