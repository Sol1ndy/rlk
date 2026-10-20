# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# Tail channel geo (azRigTail 0).
scoreboard players set @s azRigTail 0
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_az_stail,tag=rlk_mb_azs,limit=1] item set value {id:"minecraft:stripped_jungle_log",count:1}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_az_stail,tag=rlk_mb_azs,limit=1] {brightness:{block:13,sky:15}}
