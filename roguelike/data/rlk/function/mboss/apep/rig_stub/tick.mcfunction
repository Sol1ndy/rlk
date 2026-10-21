# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# @s = anchor, at it; once per game tick after the module (the pose of this tick). Missing parts respawn;
# parked: skipped (manifest park.tick "skip").
execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_ap_sbody,tag=rlk_mb_aps,limit=1] run function rlk:mboss/apep/rig_stub/spawn
execute if score @s apRigPark matches 1 run return 0
execute rotated as @s rotated ~ 0 run function rlk:mboss/apep/rig_stub/follow
scoreboard players add @s apRigT 1
function rlk:mboss/apep/rig_stub/chain
execute if score @s apRigF matches 1.. run function rlk:mboss/apep/rig_stub/flash_tick
