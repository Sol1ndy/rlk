# STUB rig (tools/mboss_butterfly/stub_rig.py): replaced by the real rig at merge time.
# Hit flash: outline for 3 t.
scoreboard players set @s bfStubY 3
execute as @e[type=minecraft:item_display,tag=rlk_mb_bfs] run data merge entity @s {Glowing:1b,glow_color_override:16777215}
