# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# @s = anchor, at it, rotated ~ 0 as it: the parts to the rest offsets of the stance (apRigStance).
execute if score @s apRigStance matches 0 positioned ^0 ^2.6 ^-0.4 run tp @e[type=minecraft:item_display,tag=rlk_mb_ap_sbody,tag=rlk_mb_aps,limit=1] ~ ~ ~ ~ 0
execute if score @s apRigStance matches 1 positioned ^0 ^3.6 ^-0.1 run tp @e[type=minecraft:item_display,tag=rlk_mb_ap_sbody,tag=rlk_mb_aps,limit=1] ~ ~ ~ ~ 0
execute if score @s apRigStance matches 0 positioned ^0 ^3.4 ^2.4 run tp @e[type=minecraft:item_display,tag=rlk_mb_ap_shead,tag=rlk_mb_aps,limit=1] ~ ~ ~ ~ 0
execute if score @s apRigStance matches 1 positioned ^0 ^6.4 ^0.3 run tp @e[type=minecraft:item_display,tag=rlk_mb_ap_shead,tag=rlk_mb_aps,limit=1] ~ ~ ~ ~ 0
execute if score @s apRigStance matches 0 positioned ^0.6 ^1.4 ^-7.4 run tp @e[type=minecraft:item_display,tag=rlk_mb_ap_stail,tag=rlk_mb_aps,limit=1] ~ ~ ~ ~ 0
execute if score @s apRigStance matches 1 positioned ^1.2 ^0.8 ^-2.4 run tp @e[type=minecraft:item_display,tag=rlk_mb_ap_stail,tag=rlk_mb_aps,limit=1] ~ ~ ~ ~ 0
