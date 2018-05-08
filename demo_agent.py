"""A random agent for starcraft."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy
import actions_modified as actions
from pysc2.agents import base_agent
#from pysc2.lib import actions as sc2_actions
from pysc2.lib import features
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
_ATTACK_UNIT = actions.FUNCTIONS.Raw_Attack_unit.id
_RAW_MOVE = actions.FUNCTIONS.Raw_Move_screen.id

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


class RawCollectMineralShards(base_agent.BaseAgent):
  """An agent specifically for solving the CollectMineralShards map."""

  def __init__(self, env):
      self.env = env
      super(RawCollectMineralShards, self).__init__()

  def step(self, obs):
    super(RawCollectMineralShards, self).step(obs)

    # Dictionary of raw_observation information
    rawobs = self.env.raw_obs()

    # List of shard objects
    neutral = rawobs["neutral_units"]

    # Own unit tags and pos
    own_tags = rawobs["own_tags"]
    own_pos = rawobs["own_pos"]

    # TODO how does it make both marines to be selected, if we are only selecting the first one from the list?
    # TODO I think that it is selecting the first marine of a random list of unit tags -
    # TODO At every step the list is not in order

    # Unit selected to perform action
    select_tag = [own_tags[0]]
    select_coords = own_pos[0]

    # Shards positions
    shards_coords = rawobs["neutral_pos"]

    # If there are no more shards left
    if len(neutral) == 0:
        return actions.FunctionCall(_NO_OP, [])

    # Calculate closest distance, and go to that shard
    closest, min_dist = None, None
    for shar_coor in shards_coords:
        dist = numpy.linalg.norm(numpy.array(select_coords) - numpy.array(shar_coor))
        if not min_dist or dist < min_dist:
            closest, min_dist = shar_coor, dist

    return actions.FunctionCall(_RAW_MOVE, [_NOT_QUEUED, select_tag, closest])

class DefeatRoaches(base_agent.BaseAgent):
  """An agent specifically for solving the DefeatRoaches map."""

  def __init__(self, env):
      self.env = env
      super(DefeatRoaches, self).__init__()

  def step(self, obs):
    super(DefeatRoaches, self).step(obs)
    #print(type(obs.observation))
    #print(obs.observation.keys())

    # TRYOUT CODE -----------------------------------------------------------------------------------------------------

    # TODO This gets the raw observation, and we can work with it using its attributes while not interfering with the
    # TODO normal observation. How should we format the actual agent?

    envobs = self.env.observation_raw()
    units = envobs.units
    own = []
    enemy = []

    # TODO This can be generalized, so every raw observation returns a detailed dictionary of self/neutral/enemyunits

    # Separate units into self/enemy lists
    # ALLIANCE CODE: 1 = Player, 2 = Ally, 3 = Neutral, 4 = Enemy
    for unit in units:
      #print ("Unit", unit.tag, "has owner", unit.owner)
      if unit.owner == 1:
        own.append(unit)
      elif unit.owner == 2:
        enemy.append(unit)

    print("Number of own units are", len(own))
    print("Number of enemy units are", len(enemy))

    # Check if there are enemies left
    if len(enemy) != 0:

      # Get the tags of all own/enemy units
      own_tags = [unit.tag for unit in own]
      enemy_tags = [unit.tag for unit in enemy]


      # Select one own unit and one enemy unit (because we don't know how to give mutiple inputs yet)
      own_id = own_tags[0]
      own_id1 = own_tags[1]
      own_id2 = own_tags[2]
      own_id3 = own_tags[3]
      own_id4 = own_tags[4]
      own_id5 = own_tags[5]
      own_id6 = own_tags[6]
      target_id = enemy_tags[0]
      target_id1 = enemy_tags[1]
      target_id2 = enemy_tags[2]
      target_id3 = enemy_tags[3]

      print("OWN IDS ARE:", own_tags)
      print("ENEMY IDS ARE:", enemy_tags)

      coord = [0, 0]
      funcs = [actions.FunctionCall(_RAW_MOVE, [_NOT_QUEUED, [own_id], coord]),
               actions.FunctionCall(_RAW_MOVE, [[1], [own_id1], coord])]
      #Return a raw_attack_unit function call
      # funcs = [actions.FunctionCall(_ATTACK_UNIT, [[1], [own_id], [target_id]]),
      #          actions.FunctionCall(_ATTACK_UNIT, [[1], [own_id1], [target_id1]]),
      #          actions.FunctionCall(_ATTACK_UNIT, [[1], [own_id2], [target_id2]]),
      #          actions.FunctionCall(_ATTACK_UNIT, [[1], [own_id3], [target_id3]]),
      #          actions.FunctionCall(_ATTACK_UNIT, [[1], [own_id4], [target_id]]),
      #          actions.FunctionCall(_ATTACK_UNIT, [[1], [own_id5], [target_id1]]),
      #          actions.FunctionCall(_ATTACK_UNIT, [[1], [own_id6], [target_id2]])]

      return funcs

    else:
      return actions.FunctionCall(_NO_OP, [])

    # -----------------------------------------------------------------------------------------------------------------

    # # Check if attack is possible
    # if _ATTACK_SCREEN in obs.observation["available_actions"]:
    #
    #   # Get matrix of environment (screen)
    #   player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
    #
    #   # Define objective, get the position of the enemies (roaches) in the matrix
    #   roach_y, roach_x = (player_relative == _PLAYER_HOSTILE).nonzero()
    #
    #   # Case where there aren't any objectives (No roaches found)
    #   if not roach_y.any():
    #     return actions.FunctionCall(_NO_OP, [])
    #
    #   index = numpy.argmax(roach_y)
    #   target = [roach_x[index], roach_y[index]]
    #   return actions.FunctionCall(_ATTACK_SCREEN, [_NOT_QUEUED, target])
    #
    #
    # elif _SELECT_ARMY in obs.observation["available_actions"]:
    #   return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
    # else:
    #   return actions.FunctionCall(_NO_OP, [])

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
