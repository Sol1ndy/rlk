# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# Body brightness 15 (apRigBright 1).
scoreboard players set @s apRigBright 1
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_ap_sbody,tag=rlk_mb_aps,limit=1] {brightness:{block:15,sky:15}}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_ap_shead,tag=rlk_mb_aps,limit=1] {brightness:{block:15,sky:15}}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_ap_stail,tag=rlk_mb_aps,limit=1] {brightness:{block:15,sky:15}}
