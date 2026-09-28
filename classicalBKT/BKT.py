from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any
import numpy as np


@dataclass
class BKT:
    skill_names: list[str]
    prior: float = 0.10
    learn: float = 0.20
    guess: float = 0.20
    slip: float = 0.10

    def __post_init__(self):
        if not self.skill_names:
            raise ValueError("skill_names cannot be empty")

        for value in (self.prior, self.learn, self.guess, self.slip):
            if not 0 <= value <= 1:
                raise ValueError("BKT parameters must be between 0 and 1")

        self.skill_to_index = {
            name: i for i, name in enumerate(self.skill_names)
        }

        self.state = np.full(
            len(self.skill_names),
            self.prior,
            dtype=np.float64
        )

    def Update(self, previous_state, data, correctness):
        state = np.array(
            [
                previous_state.get(skill, self.prior)
                for skill in self.skill_names
            ],
            dtype=np.float64
        )

        for skill in data["skill"]:
            index = self.skill_to_index[skill]
            p_known = state[index]

            if correctness:
                probability = (
                    p_known * (1.0 - self.slip)
                    + (1.0 - p_known) * self.guess
                )
                posterior = (
                    p_known * (1.0 - self.slip)
                ) / probability
            else:
                probability = (
                    p_known * self.slip
                    + (1.0 - p_known) * (1.0 - self.guess)
                )
                posterior = (
                    p_known * self.slip
                ) / probability

            state[index] = posterior + (
                1.0 - posterior
            ) * self.learn

        return {
            skill: float(state[index])
            for skill, index in self.skill_to_index.items()
        }

