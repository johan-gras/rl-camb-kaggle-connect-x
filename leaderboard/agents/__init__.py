from collections import namedtuple

from .negamax_agent.negamax_agent import Negamax
from .random_agent import random_agent

AgentTuple = namedtuple("AgentTuple", ['func', 'user', 'is_baseline'])

REGISTERED_AGENTS = {
    'Random': AgentTuple(random_agent.act, user='Kaggle', is_baseline=True),
    'Negamax ply-1': AgentTuple(Negamax(max_depth=1), user='Kaggle', is_baseline=True),
    'Negamax ply-2': AgentTuple(Negamax(max_depth=2), user='Kaggle', is_baseline=True),
    'Negamax ply-4': AgentTuple(Negamax(max_depth=4), user='Kaggle', is_baseline=True),
    'Negamax ply-5': AgentTuple(Negamax(max_depth=5), user='Kaggle', is_baseline=True),
}
