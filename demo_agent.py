"""A random agent for starcraft."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy

from pysc2.agents import base_agent
from pysc2.lib import actions

from pysc2.lib import actions as sc2_actions
from pysc2.lib import features
from pysc2.lib import actions

import common

import numpy as np

# Features of screen, unit type, selected unit
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_SELECTED = features.SCREEN_FEATURES.selected.index

# Indices of units on screen
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4

# Standby ID
_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_UNIT_ID = 1

_CONTROL_GROUP_SET = 1
_CONTROL_GROUP_RECALL = 0

# IDs of actions
_SELECT_CONTROL_GROUP = actions.FUNCTIONS.select_control_group.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_SELECT_UNIT = actions.FUNCTIONS.select_unit.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id

_NOT_QUEUED = [0]
_SELECT_ALL = [0]

class MoveToBeacon(base_agent.BaseAgent):
  """An agent specifically for solving the MoveToBeacon map."""

  def step(self, obs):
    super(MoveToBeacon, self).step(obs)
    if _MOVE_SCREEN in obs.observation["available_actions"]:
      player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
      neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
      if not neutral_y.any():
        return actions.FunctionCall(_NO_OP, [])
      target = [int(neutral_x.mean()), int(neutral_y.mean())]
      return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, target])
    else:
      return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])


class CollectMineralShards(base_agent.BaseAgent):
  """An agent specifically for solving the CollectMineralShards map."""

  def step(self, obs):
    super(CollectMineralShards, self).step(obs)
    if _MOVE_SCREEN in obs.observation["available_actions"]:
      player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
      neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
      player_y, player_x = (player_relative == _PLAYER_FRIENDLY).nonzero()
      if not neutral_y.any() or not player_y.any():
        return actions.FunctionCall(_NO_OP, [])
      player = [int(player_x.mean()), int(player_y.mean())]
      closest, min_dist = None, None
      for p in zip(neutral_x, neutral_y):
        dist = numpy.linalg.norm(numpy.array(player) - numpy.array(p))
        if not min_dist or dist < min_dist:
          closest, min_dist = p, dist
      return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, closest])
    else:
      return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])


class DefeatRoaches(base_agent.BaseAgent):
  """An agent specifically for solving the DefeatRoaches map."""

  # Added by @danielfirebanks - optional init function if we want to have access to the environment in the agent creation
  # TODO Should the agent have access to the environment, just to have the observation_raw?

  def __init__(self, env):
      self.env = env
      super(DefeatRoaches, self).__init__()

  def step(self, obs):
    super(DefeatRoaches, self).step(obs)
    #print(type(obs.observation))
    print(obs.observation.keys())

    # TODO This gets the raw observation, and we can work with it using its attributes while not interfering with the
    # TODO normal observation. How should we format the actual agent?

    envobs = self.env.observation_raw()

    # Check if attack is possible
    if _ATTACK_SCREEN in obs.observation["available_actions"]:

      # Get matrix of environment (screen)
      player_relative = obs.observation["screen"][_PLAYER_RELATIVE]

      # Define objective, get the position of the enemies (roaches) in the matrix
      roach_y, roach_x = (player_relative == _PLAYER_HOSTILE).nonzero()

      # Case where there aren't any objectives (No roaches found)
      if not roach_y.any():
        return actions.FunctionCall(_NO_OP, [])

      index = numpy.argmax(roach_y)
      target = [roach_x[index], roach_y[index]]
      return actions.FunctionCall(_ATTACK_SCREEN, [_NOT_QUEUED, target])


    elif _SELECT_ARMY in obs.observation["available_actions"]:
      return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
    else:
      return actions.FunctionCall(_NO_OP, [])

class MarineAgent(base_agent.BaseAgent):
  """A random agent for starcraft."""
  demo_replay = []

  def __init__(self, env):
      self.env = env
      super(MarineAgent, self).__init__()

  def step(self, obs):
    super(MarineAgent, self).step(obs)

    #1. Select marine!
    obs, screen, player = common.select_marine(self.env, [obs])

    player_relative = obs[0].observation["screen"][_PLAYER_RELATIVE]

    enemy_y, enemy_x = (player_relative == _PLAYER_HOSTILE).nonzero()


    #2. Run away from nearby enemy
    closest, min_dist = None, None

    if(len(player) == 2):
      for p in zip(enemy_x, enemy_y):
        dist = np.linalg.norm(np.array(player) - np.array(p))
        if not min_dist or dist < min_dist:
          closest, min_dist = p, dist


    #3. Sparse!
    friendly_y, friendly_x = (player_relative == _PLAYER_FRIENDLY).nonzero()

    closest_friend, min_dist_friend = None, None
    if(len(player) == 2):
      for p in zip(friendly_x, friendly_y):
        dist = np.linalg.norm(np.array(player) - np.array(p))
        if not min_dist_friend or dist < min_dist_friend:
          closest_friend, min_dist_friend = p, dist

    if(min_dist != None and min_dist <= 7):

      obs, new_action = common.marine_action(self.env, obs, player, 2)

    elif(min_dist_friend != None and min_dist_friend <= 3):

      sparse_or_attack = np.random.randint(0,2)

      obs, new_action = common.marine_action(self.env, obs, player, sparse_or_attack)

    else:

      obs, new_action = common.marine_action(self.env, obs, player, 1)

    return new_action[0]
