import sys
import absl.flags as flags
import sc2env_modified as sc2_env
#from pysc2.lib import actions
import actions_modified as actions
from pysc2.env import run_loop
import demo_agent

_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_SELECT_ALL = [0]
_NOT_QUEUED = [0]

step_mul = 16
steps = 1000

FLAGS = flags.FLAGS

def run_action(demo_agent):
    FLAGS(sys.argv)

    with sc2_env.SC2Env(
        map_name="CollectMineralShards",
        step_mul=step_mul,
        visualize=True,
        game_steps_per_episode=steps*step_mul) as env:

        agent = demo_agent
        agent.env = env

        run_loop.run_loop([agent], env, steps)


if __name__ == '__main__':
  daagent = demo_agent.RawCollectMineralShards(None)
  run_action(demo_agent=daagent)
