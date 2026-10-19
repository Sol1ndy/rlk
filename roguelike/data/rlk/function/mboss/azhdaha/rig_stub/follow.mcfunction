# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# @s = anchor, at it, rotated ~ 0 as it: the parts to their offsets (tail-only: the tail stands on the anchor).
execute positioned ^0 ^2.9 ^-0.3 run tp @e[type=minecraft:item_display,tag=rlk_mb_az_sbody,tag=rlk_mb_azs,limit=1] ~ ~ ~ ~ 0
execute positioned ^0 ^1.6 ^4.6 run tp @e[type=minecraft:item_display,tag=rlk_mb_az_shead,tag=rlk_mb_azs,limit=1] ~ ~ ~ ~ 0
execute if score @s azRigState matches 2 run tp @e[type=minecraft:item_display,tag=rlk_mb_az_stail,tag=rlk_mb_azs,limit=1] ~ ~4.4 ~ ~ 0
execute unless score @s azRigState matches 2 positioned ^0 ^1.6 ^-10.3 run tp @e[type=minecraft:item_display,tag=rlk_mb_az_stail,tag=rlk_mb_azs,limit=1] ~ ~ ~ ~ 0
execute positioned ^0 ^2.15 ^5.95 run tp @e[type=minecraft:item_display,tag=rlk_mb_az_seyes,tag=rlk_mb_azs,limit=1] ~ ~ ~ ~ 0
