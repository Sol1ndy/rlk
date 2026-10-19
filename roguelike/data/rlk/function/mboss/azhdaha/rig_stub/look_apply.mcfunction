# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# The stored looks and state again (spawn, reload).
execute if score @s azRigLegs matches 0 run function rlk:mboss/azhdaha/rig_stub/look/legs/geo
execute if score @s azRigLegs matches 1 run function rlk:mboss/azhdaha/rig_stub/look/legs/hydro
execute if score @s azRigLegs matches 2 run function rlk:mboss/azhdaha/rig_stub/look/legs/pyro
execute if score @s azRigTail matches 0 run function rlk:mboss/azhdaha/rig_stub/look/tail/geo
execute if score @s azRigTail matches 1 run function rlk:mboss/azhdaha/rig_stub/look/tail/cryo
execute if score @s azRigTail matches 2 run function rlk:mboss/azhdaha/rig_stub/look/tail/electro
execute if score @s azRigState matches 0 run function rlk:mboss/azhdaha/rig_stub/state/normal
execute if score @s azRigState matches 1 run function rlk:mboss/azhdaha/rig_stub/state/burrowed
execute if score @s azRigState matches 2 run function rlk:mboss/azhdaha/rig_stub/state/tail_only
