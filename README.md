# MultiAgent-Systems-StarCraft2-Spring-AIResearch

Contains:
- Siraj Raval's code for SC2 demos
- New modified code based on the pysc2 API to work with Raw Interface

Modifications:
- Added observation_raw() method in s2env_modified.py to get observation in raw format and ready to access
- Added isAvailable() method in s2env_modified.py to check if specific action is available for current state
- Added transform_raw() method in s2env_modified.py to setup raw actions
- Added cmd_raw_unit(), cmd_raw_map(), cmd_raw_quick(). cmd_raw_autocast() in actions_modified.py to setup raw_commands, including setting up in ArgumentTypes and Functions. 
- Updated Functions, ArgumentTypes, Arguments, etc.
- Generalized usage of raw actions and observations - Currently can send actions and receive observations for almost all possible actions.
- Created method raw_obs() that returns an observation in the form of a dictionary, containing all the important information that an agent could use to interact with the raw interface, such as unit tags, 2D map positions, etc.

TODO
- [ ] Add calls to cmd_raw_unit() in actions_modified, in the list FUNCTIONS
- [ ] Fix run_loop_modified and figure out how to read multiple action requests in one step call
- [ ] Figure out how to make several agents get selected and appended to the unit_tags list of an ActionRaw, such that they can all perform the same action
