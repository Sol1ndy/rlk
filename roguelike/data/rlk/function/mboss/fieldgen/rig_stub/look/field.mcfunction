# STUB rig (tools/mboss_fieldgen/stub_rig.py): replaced by the real rig (wip/fg-rig) at merge time.
# Look field.
scoreboard players set @s fgRigL 2
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_fg_core,tag=rlk_mb_fgs,limit=1] {Glowing:1b,glow_color_override:10258152}
data modify entity @e[type=minecraft:item_display,tag=rlk_mb_fg_core,tag=rlk_mb_fgs,limit=1] item set value {id:"minecraft:gold_block",count:1}
