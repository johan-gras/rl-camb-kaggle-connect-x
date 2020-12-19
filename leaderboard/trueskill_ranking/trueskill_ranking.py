import random

import trueskill
from tqdm import tqdm


def compute_leaderboard(agents_name, evaluate_agents, sigma_threshold=1.):
    # Allows sigma to always converge
    trueskill.setup(tau=0.)
    # Create a rating object for each agents
    ratings = {agent_name: trueskill.Rating() for agent_name in agents_name}

    pbar = tqdm()
    pbar.set_description("Computing TrueSkill leaderboard")
    while True:
        # Find agent with bigger sigma
        agent_a, sigma_max = None, -1
        for agent_name, rating in ratings.items():
            if rating.sigma > sigma_max:
                agent_a, sigma_max = agent_name, rating.sigma
        pbar.set_postfix({"sigma_max": sigma_max})
        # Stop if all sigma are smaller than the sigma_threshold
        if sigma_max < sigma_threshold:
            break
        # Find another agent at ramdom
        agent_b = random.choice([agent_name for agent_name in ratings if agent_name != agent_a])
        # Evaluate agents together and update their ratings
        result = evaluate_agents(agent_a, agent_b)
        drawn = result == 0
        if result >= 0:
            ratings[agent_a], ratings[agent_b] = trueskill.rate_1vs1(ratings[agent_a], ratings[agent_b], drawn=drawn)
        else:
            ratings[agent_b], ratings[agent_a] = trueskill.rate_1vs1(ratings[agent_b], ratings[agent_a], drawn=drawn)
        pbar.update()

    pbar.close()
    leaderboard = list(sorted(ratings.items(), key=lambda r: r[1].mu, reverse=True))
    return leaderboard
