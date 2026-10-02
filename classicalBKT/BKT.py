from __future__ import annotations

from dataclasses import dataclass

@dataclass
class BKT:
    learn: float = 0.20
    guess: float = 0.20
    slip: float = 0.10

    def Update(self, previous_state, data, correctness): 
        state = previous_state.copy()

        for skill in data["skill"]:
            p_known = state[skill]

            if correctness:
                known_correct = p_known * (1.0 - self.slip)
                unknown_correct = (1.0 - p_known) * self.guess

                p = known_correct / (known_correct + unknown_correct)

                state[skill] = p + (1.0 - p) * self.learn

            else:
                known_incorrect = p_known * self.slip
                unknown_incorrect = (1.0 - p_known) * (1.0 - self.guess)

                p = known_incorrect / (known_incorrect + unknown_incorrect)

                state[skill] = p

        return state

