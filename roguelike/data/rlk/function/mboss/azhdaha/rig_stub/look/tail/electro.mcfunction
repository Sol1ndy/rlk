# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# Tail channel electro (azRigTail 2).
scoreboard players set @s azRigTail 2
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_az_stail,tag=rlk_mb_azs,limit=1] item set value {id:"minecraft:purpur_pillar",count:1}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_az_stail,tag=rlk_mb_azs,limit=1] {brightness:{block:15,sky:15}}
