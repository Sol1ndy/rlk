# @s = player. The perfect dodge's red-pink glow on the whole body: every body part of the showing rig (the rig character's,
# or the stand-in rig) is tinted red-pink (the part models' tint), drawn at full brightness and outlined in pink.
scoreboard players set @s pbTint 1
execute as @e[tag=rlk_pm,tag=!rlk_pm_weapon] run data merge entity @s {Glowing:1b,glow_color_override:16747660,brightness:{sky:15,block:15},shadow_strength:0.99f,item:{components:{"minecraft:custom_model_data":{colors:[16755376]}}}}
execute as @e[tag=rlk_pl,tag=!rlk_pl_weapon] run data merge entity @s {Glowing:1b,glow_color_override:16747660,brightness:{sky:15,block:15},shadow_strength:0.99f,item:{components:{"minecraft:custom_model_data":{colors:[16755376]}}}}
