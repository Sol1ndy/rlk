# STUB rig (tools/mboss_fieldgen/stub_rig.py): replaced by the real rig (wip/fg-rig) at merge time.
# @s = anchor, at it; every game tick (after the AI). Missing parts respawn.
execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_fg_ring,tag=rlk_mb_fgs,limit=1] run function rlk:mboss/fieldgen/rig_stub/spawn
execute if score @s fgRigF matches 0 rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/rig_stub/follow/dormant
execute if score @s fgRigF matches 1 rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/rig_stub/follow/cruise
execute if score @s fgRigF matches 2 rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/rig_stub/follow/field
execute if score @s fgRigF matches 3 rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/rig_stub/follow/coreup
execute if score @s fgRigF matches 4 rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/rig_stub/follow/tower
execute if score @s fgRigF matches 5 rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/rig_stub/follow/laser
execute if score @s fgRigF matches 6 rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/rig_stub/follow/deployed
scoreboard players add @s fgRigT 1
function rlk:mboss/fieldgen/rig_stub/run
execute if score @s fgRigY matches 1.. run function rlk:mboss/fieldgen/rig_stub/flash_tick
