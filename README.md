# RL Cambridge Kaggle Competition Project

This is a repository for members of the Cambridge (UK) Reinforcement Learning Meetup to create agents and compete in games of connect-X, an environment introduced by Kaggle. See for more details: https://www.kaggle.com/c/connectx

## Setup

### Environment

The requirements.txt can be used to setup the dependencies.

A conda environment is also available which includes the Kaggle Connect-X RL environment and all modules that were available in the original competition:
- Python standard libraries (python 3.6)
- pytorch
- numpy
- scipy
- gym
- kaggle-environments==0.1.6 (more recent versions threw an error when importing `kaggle_environments`

To get the conda environment that allows you to use the kaggle environment, follow these steps. Check out README.md in `conda_envs` for more information on downloading `anaconda` before doing the below, if you don't have it already.

```bash
cd conda_env
conda create -f conda_env.yml
conda activate common
cd ..
```

### Getting started

After setting up the environment, try:
```bash
source setup_python_path.sh
python check_run.py
```

The `check_run.py` script checks that your environment is functioning with the environment correctly, and gives key examples on how to interact with the python code and get started. It is largely a copy-paste of the codeblocks available in the notebook: https://www.kaggle.com/ajeffries/connectx-getting-started

## Competing

As per the competition rules below, it's recommended you don't share your code if you're planning to compete in the Kaggle Competition "unless it's made available at no cost via the official competition forums" (see link below). I'm not totally sure that's the meaning of the rule, but that seems lik the safest interpretation. 

https://www.kaggle.com/c/connectx/rules

Now the rules bit is over... We can use this environment to compete between our own agents! If you have an agent that is in submittable format, we can compete. Submittable format means to have an entirely encapsulated function called `my_agent(observation, configuration)`. This is verified with `scripts/agent_runner my_agent_file.py`, or by jumping straight in and trying the below:

```bash
scripts/evaluate_agents.py agent1_file.py [agent2_file.py negamax random]
```

`example_submission/` shows the example agent and the example code used to create the submittable file (reproduced in `scripts/submit_agent.py`), as-provided by Kaggle.

`q_learning/` has an example written by the repo author that is runnable with the `evaluate_agents.py` script, but I have not yet verified that it will be runnable in a proper kaggle submission (the main uncertainty is whether the model state dict .pt file is submittable, as I have seen some examples where the state dict is written out as a variable within the function. I hope this won't be necessary, as it seems like a big pain!

# TrueSkill leaderboard
A leaderboard is a good way to represent the performance of 2 or more agents.
Kaggle has built their leaderboard using a variant of [TrueSkill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/), a kind of Elo algorithm developed by Microsoft:
> Our ranking system takes more inspiration from TrueSkill than Elo for a variety of reasons, some being that TrueSkill has better native support for ties (which are more common in our other Simulation competition, ConnectX) and multiplayer games.
> [Kaggle Staff](https://www.kaggle.com/c/halite/discussion/160083)

The [leaderboard package](leaderboard) generates a homemade leaderboard based on the TrueSkill algorithm:

Agent | User | TrueSkill | W/L/D | Baseline
--- | --- | --- | --- | ---
Negamax ply-4 | Kaggle | 31.16 | 72/3/19 | ✔
Negamax ply-5 | Kaggle | 29.58 | 68/11/17 | ✔
Negamax ply-2 | Kaggle | 24.84 | 38/30/14 | ✔
Negamax ply-1 | Kaggle | 20.46 | 15/56/17 | ✔
Random | Kaggle | 17.50 | 2/95/17 | ✔

## How to compute the leaderboard?
To compute the leaderboard:
```
cd leaderboard
python make_leaderboard.py 
```
This will compute the leaderboard based on the current [REGISTERED_AGENTS](leaderboard/agents/__init__.py) configuration.

`sigma_threshold` is a parameter that controls the trade-off between precision of the leaderboard values and speed of computation (smaller: more precision. bigger: faster).
By default `sigma_threshold=0.5`, you can control this parameter as such:

`python make_leaderboard.py  --sigma_threshold 1.`

## Adding my agent
You can add your agent by saving your code in the [agents package](leaderboard/agents) and adding an entry in the [REGISTERED_AGENTS](leaderboard/agents/__init__.py) configuration:

```
REGISTERED_AGENTS = {
    'Random': AgentTuple(random_agent.act, is_baseline=True),
    'Negamax ply-0': AgentTuple(negamax_agent.Negamax(max_depth=0), is_baseline=True),
    'Negamax ply-6': AgentTuple(negamax_agent.Negamax(max_depth=6), is_baseline=True),
}
```
If your agent is ml/rl based write `is_baseline=False` instead. Non-learning-based agents are accepted but just for baseline purposes.