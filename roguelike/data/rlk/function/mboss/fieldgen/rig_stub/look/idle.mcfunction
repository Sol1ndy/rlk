# STUB rig (tools/mboss_fieldgen/stub_rig.py): replaced by the real rig (wip/fg-rig) at merge time.
# Look idle.
scoreboard players set @s fgRigL 0
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_fg_core,tag=rlk_mb_fgs,limit=1] {Glowing:0b}
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_fg_core,tag=rlk_mb_fgs,limit=1] item set value {id:"minecraft:gold_block",count:1}
