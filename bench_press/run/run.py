import argparse
import sys

from bench_press.utils.infra import str_to_class
from omegaconf import OmegaConf


def run(conf, num_rollouts):
    agent_class = str_to_class(conf.agent.type)
    agent = agent_class(conf)

    policy_class = str_to_class(conf.policy.type)
    policy = policy_class(conf.policy)

    for rollout_idx in range(num_rollouts):
        agent.rollout(policy, rollout_idx)
    agent.env.reset()
    agent.env.clean_up()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run policies on testbench')
    parser.add_argument('config_file', action='store')
    parser.add_argument('num_rollouts', action='store', type=int)
    args = parser.parse_args()

    assert 1 <= args.num_rollouts, 'number of rollouts should be positive'
    try:
        conf = OmegaConf.load(args.config_file)
    except:
        print('Failed to load config, exiting now...')
        sys.exit()

    run(conf, args.num_rollouts)
