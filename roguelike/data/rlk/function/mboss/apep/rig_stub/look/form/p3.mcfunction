# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# Look channel form = p3 (apRigForm 1).
scoreboard players set @s apRigForm 1
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_ap_sbody,tag=rlk_mb_aps,limit=1] item set value {id:"minecraft:flowering_azalea_leaves",count:1}
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_ap_shead,tag=rlk_mb_aps,limit=1] item set value {id:"minecraft:spore_blossom",count:1}
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_ap_stail,tag=rlk_mb_aps,limit=1] item set value {id:"minecraft:mangrove_roots",count:1}
