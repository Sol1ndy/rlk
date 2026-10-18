# STUB rig (tools/mboss_butterfly/stub_rig.py): replaced by the real rig at merge time.
# @s = anchor, at it; every game tick. Missing parts respawn.
execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_bfs,tag=rlk_mb_bf_body,limit=1] run function rlk:mboss/butterfly/rig_stub/spawn
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/rig_stub/follow
scoreboard players add @s bfStubT 1
function rlk:mboss/butterfly/rig_stub/run
execute if score @s bfStubY matches 1.. run function rlk:mboss/butterfly/rig_stub/flash_tick
