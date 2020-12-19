from collections import defaultdict

import click
from kaggle_environments import make, evaluate

from agents import REGISTERED_AGENTS
from trueskill_ranking import compute_leaderboard


@click.command()
@click.option('--sigma_threshold', default=0.5)
def make_leaderboard(sigma_threshold):
    """Compute the leaderboard with TrueSkill rating and create the leaderboard in README.md"""
    stats_agents = defaultdict(lambda: {"win": 0, "lose": 0, "draw": 0})

    def evaluate_agents(agent_a, agent_b):
        """Evaluate a vs b and b vs a"""
        agent_a_func, agent_b_func = REGISTERED_AGENTS[agent_a].func, REGISTERED_AGENTS[agent_b].func
        a_vs_b = evaluate("connectx", [agent_a_func, agent_b_func], num_episodes=1)
        b_vs_a = evaluate("connectx", [agent_b_func, agent_a_func], num_episodes=1)
        score_a = a_vs_b[0][0] + b_vs_a[0][1]

        if score_a > 0:  # agent_a win 1 or 2 games
            stats_agents[agent_a]["win"] += 1
            stats_agents[agent_b]["lose"] += 1
            return 1
        elif score_a < 0:  # agent_b win 1 or 2 games
            stats_agents[agent_b]["win"] += 1
            stats_agents[agent_a]["lose"] += 1
            return -1
        else:
            stats_agents[agent_a]["draw"] += 1
            stats_agents[agent_b]["draw"] += 1
            return 0

    # Check agents are working properly
    for agent_name, agent in REGISTERED_AGENTS.items():
        env = make("connectx", debug=True)
        env.run([agent.func, agent.func])
        assert env.state[0].status == env.state[1].status == "DONE", f"{agent_name} not working properly.\n{env.state}"

    # Compute the leaderboard with TrueSkill ranking
    leaderboard = compute_leaderboard(list(REGISTERED_AGENTS), evaluate_agents, sigma_threshold=sigma_threshold)
    print(leaderboard)

    # Write leaderboard in README.md
    leaderboard_table = ["# Leaderboard\n",
                         "Agent | User | TrueSkill | W/L/D | Baseline\n",
                         "--- | --- | --- | --- | ---\n"]
    for agent_name, rating in leaderboard:
        agent = REGISTERED_AGENTS[agent_name]
        stat = stats_agents[agent_name]
        leaderboard_table += f"{agent_name} | " \
                             f"{agent.user} | " \
                             f"{rating.mu:.2f} | " \
                             f"{stat['win']}/{stat['lose']}/{stat['draw']} | " \
                             f"{'✔' if agent.is_baseline else ''}\n"
    with open("README.md", "w", encoding='utf-8') as f:
        f.writelines(leaderboard_table)


if __name__ == '__main__':
    make_leaderboard()
