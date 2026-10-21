# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# Look channel core_glow = idle (apRigGlow 0).
scoreboard players set @s apRigGlow 0
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_ap_sbody,tag=rlk_mb_aps,limit=1] {Glowing:0b,glow_color_override:15065431}
