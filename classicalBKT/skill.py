import random
import math

DEBUG = False

# Wrap class of skill
class Skill:
    vector: list[float]

    def __init__(self, vector):
        self.vector = vector

# L2 norm, Sum(x^2) = 1
def L2norm(v: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in v))
    if norm == 0:
        raise ValueError("No matching skills found")
    return [1.0 * x / norm for x in v]

# auto adapt to with/without weight data
def to_vector(label: list[str], skills: list[str] | dict):
    v = [0.0] * len(label); 
    label_idx: dict[str, int] = {
        lb: idx
        for idx, lb in enumerate(label)
    }

    if isinstance(skills, dict):
        for lb, w in skills.items():
            if not (isinstance(lb,str) and isinstance(w,(int,float))):
                raise TypeError("Wrong skill template")

            v[label_idx[lb]] = 1.0 * w

    elif isinstance(skills, list):
        for lb in skills:
            if not isinstance(lb,str):
                raise TypeError("Wrong skill template")

            v[label_idx[lb]] = 1.0

    else:
        raise TypeError("Wrong question template")
    
    return L2norm(v)

# build all skill vectors for each question in list
def build_Skill(label: list[str], questions: list) -> list[Skill]:
    lst = []
    for q in questions:
        lst.append(Skill(to_vector(label, q["skill"]))) 
    return lst

# cosine similarity: cos = xy / |x| |y| 
# current_state should never be L2 norm, vectors are already L2 normed
def cosine_similarity(current_state: list[float], v:list[float]):
    l = len(current_state); sum = 0.0; 

    norm_state = L2norm(current_state); 

    for i in range(l):
        sum += norm_state[i] * v[i]

    return sum

# choose next question idx based on current state
# randomly choose bottom K cosine similarity to practice unfamiliar topics
def choose_index(current_state, skills: list[Skill], K = 1):
    s = list(current_state.values())

    similarities = []
    
    for i in range(len(skills)):
        skill = skills[i]
        dist = cosine_similarity(s, skill.vector)
        similarities.append((dist,i))

    similarities.sort()
    K = min(K, len(similarities))
    _, idx = random.choice(similarities[:K])

    if DEBUG:
        print(s)
        for i in range(K):
            print("Skill vector:", skills[similarities[i][1]].vector, "Similarity:",similarities[i][0])
    
    return idx