# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# @s = anchor, at it; once per game tick after the module (the pose of this tick). Missing parts respawn.
execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_az_sbody,tag=rlk_mb_azs,limit=1] run function rlk:mboss/azhdaha/rig_stub/spawn
execute rotated as @s rotated ~ 0 run function rlk:mboss/azhdaha/rig_stub/follow
scoreboard players add @s azRigT 1
function rlk:mboss/azhdaha/rig_stub/chain
execute if score @s azRigF matches 1.. run function rlk:mboss/azhdaha/rig_stub/flash_tick
