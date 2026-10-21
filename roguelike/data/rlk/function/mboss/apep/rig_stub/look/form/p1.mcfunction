# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# Look channel form = p1 (apRigForm 0).
scoreboard players set @s apRigForm 0
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_ap_sbody,tag=rlk_mb_aps,limit=1] item set value {id:"minecraft:moss_block",count:1}
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_ap_shead,tag=rlk_mb_aps,limit=1] item set value {id:"minecraft:pitcher_plant",count:1}
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_ap_stail,tag=rlk_mb_aps,limit=1] item set value {id:"minecraft:stripped_mangrove_log",count:1}
