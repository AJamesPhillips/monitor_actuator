
# Multi node

A repo to contain code for setting up and running a system(s) for aiding in
monitoring and actuating.

Example use cases include:

* temperature monitor(s) for warning fridge/freezer failure
* webcam(s) for taking periodic photos of the lab as extra aides to protecting
  the occupants and the space, as well as potential usage stats to inform
  debate.
* sense RFID
* enabled / disable equipment


## Tests

    multi-node $  PYTHONPATH=`pwd` pytest tests/**/* --pdb
