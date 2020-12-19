"""Some tests to checks that trueskill_ranking behave correctly for deterministic and non-deterministic results."""

import random

from leaderboard.trueskill_ranking import compute_leaderboard

# Mapping: agent_name -> agent_score
AGENTS = {
    "TheBest": 5,
    "NotBad": 4,
    "Ex": 3,
    "Aequo": 3,
    "CouldDoBetter": 2,
    "Loser": 1
}


def fake_evaluate_agents_deterministic(agent_a, agent_b):
    score_a, score_b = AGENTS[agent_a], AGENTS[agent_b]
    if score_a > score_b:
        return 1
    elif score_b > score_a:
        return -1
    else:
        return 0


def test_leaderboard_order_is_correct_deterministic():
    l_agents = list(AGENTS)
    random.shuffle(l_agents)  # Add some variance

    leaderboard = compute_leaderboard(l_agents, fake_evaluate_agents_deterministic, sigma_threshold=2.)
    leaderboard_names = [agent_name for agent_name, _ in leaderboard]

    expected_leaderboard_names_1 = ["TheBest", "NotBad", "Ex", "Aequo", "CouldDoBetter", "Loser"]
    expected_leaderboard_names_2 = ["TheBest", "NotBad", "Aequo", "Ex", "CouldDoBetter", "Loser"]
    assert leaderboard_names == expected_leaderboard_names_1 or \
           leaderboard_names == expected_leaderboard_names_2


def fake_evaluate_agents_non_deterministic(agent_a, agent_b):
    score_a, score_b = AGENTS[agent_a], AGENTS[agent_b]
    threshold = score_a - score_b
    value = random.randint(-4, 4)
    if value > threshold:  # agent_b win
        return -1
    elif value < threshold:  # agent_a win
        return 1
    else:  # draw
        return 0


def test_leaderboard_order_is_correct_non_deterministic():
    l_agents = list(AGENTS)
    random.shuffle(l_agents)  # Add some variance

    leaderboard = compute_leaderboard(list(AGENTS), fake_evaluate_agents_non_deterministic, sigma_threshold=0.5)
    leaderboard_names = [agent_name for agent_name, _ in leaderboard]

    expected_leaderboard_names_1 = ["TheBest", "NotBad", "Ex", "Aequo", "CouldDoBetter", "Loser"]
    expected_leaderboard_names_2 = ["TheBest", "NotBad", "Aequo", "Ex", "CouldDoBetter", "Loser"]
    assert leaderboard_names == expected_leaderboard_names_1 or \
           leaderboard_names == expected_leaderboard_names_2
