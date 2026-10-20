# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# Death seal: every part turns to stone, darker (base looks at brightness -3).
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_az_sbody,tag=rlk_mb_azs,limit=1] item set value {id:"minecraft:stone",count:1}
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_az_shead,tag=rlk_mb_azs,limit=1] item set value {id:"minecraft:stone",count:1}
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_az_stail,tag=rlk_mb_azs,limit=1] item set value {id:"minecraft:stone",count:1}
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_az_seyes,tag=rlk_mb_azs,limit=1] item set value {id:"minecraft:stone",count:1}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_az_sbody,tag=rlk_mb_azs,limit=1] {brightness:{block:10,sky:12}}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_az_shead,tag=rlk_mb_azs,limit=1] {brightness:{block:10,sky:12}}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_az_stail,tag=rlk_mb_azs,limit=1] {brightness:{block:10,sky:12}}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_az_seyes,tag=rlk_mb_azs,limit=1] {brightness:{block:10,sky:12}}
