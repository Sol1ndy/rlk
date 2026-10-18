# STUB rig (tools/mboss_fieldgen/stub_rig.py): replaced by the real rig (wip/fg-rig) at merge time.
# Hit flash: outline for 3 t.
scoreboard players set @s fgRigY 3
execute as @e[type=minecraft:item_display,tag=rlk_mb_fgs] run data merge entity @s {Glowing:1b,glow_color_override:16777215}
