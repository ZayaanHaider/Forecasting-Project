from __future__ import annotations

import numpy as np
from random import choices

STATES = ["Sunny", "Cloudy", "Rain"]
TRANSITION_MATRIX = np.array([
    [0.79, 0.13, 0.08],
    [0.16, 0.63, 0.21],
    [0.08, 0.17, 0.75],
], dtype=float)


def validate_matrix(matrix: np.ndarray) -> None:
    row_sums = matrix.sum(axis=1)
    if not np.allclose(row_sums, 1.0):
        raise ValueError(f"Each row must sum to 1. Row sums were: {row_sums}")


def state_vector(start_state: str) -> np.ndarray:
    if start_state not in STATES:
        raise ValueError(f"Invalid state: {start_state}")
    vector = np.zeros(len(STATES), dtype=float)
    vector[STATES.index(start_state)] = 1.0
    return vector


def simulate_chain(start_state: str, days: int) -> list[str]:
    if days < 1:
        raise ValueError("days must be at least 1")
    validate_matrix(TRANSITION_MATRIX)

    chain = [start_state]
    current = start_state
    for _ in range(days - 1):
        weights = TRANSITION_MATRIX[STATES.index(current)].tolist()
        current = choices(STATES, weights=weights, k=1)[0]
        chain.append(current)
    return chain


def daily_probabilities(start_state: str, days: int) -> list[np.ndarray]:
    if days < 1:
        raise ValueError("days must be at least 1")
    validate_matrix(TRANSITION_MATRIX)

    probs = [state_vector(start_state)]
    current = state_vector(start_state)
    for _ in range(days - 1):
        current = current @ TRANSITION_MATRIX
        probs.append(current.copy())
    return probs


def final_day_probabilities(start_state: str, days: int) -> np.ndarray:
    return daily_probabilities(start_state, days)[-1]


def monte_carlo_summary(start_state: str, days: int, simulations: int) -> dict[str, object]:
    if simulations < 1:
        raise ValueError("simulations must be at least 1")

    end_state_counts = {state: 0 for state in STATES}
    total_counts = {state: 0 for state in STATES}

    for _ in range(simulations):
        chain = simulate_chain(start_state, days)
        end_state_counts[chain[-1]] += 1
        for state in chain:
            total_counts[state] += 1

    total_observations = simulations * days
    end_state_percents = {
        state: (count / simulations) * 100 for state, count in end_state_counts.items()
    }
    long_run_percents = {
        state: (count / total_observations) * 100 for state, count in total_counts.items()
    }

    return {
        "end_state_counts": end_state_counts,
        "end_state_percents": end_state_percents,
        "long_run_percents": long_run_percents,
    }


def steady_state_distribution(iterations: int = 250) -> np.ndarray:
    validate_matrix(TRANSITION_MATRIX)
    distribution = np.array([1 / 3, 1 / 3, 1 / 3], dtype=float)
    for _ in range(iterations):
        distribution = distribution @ TRANSITION_MATRIX
    return distribution
