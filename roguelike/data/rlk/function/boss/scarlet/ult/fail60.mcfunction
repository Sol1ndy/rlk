# The 60 % fail hit (ULT60_LETHAL false; position = the impact point, the dive on the player): 500 per mille
# of the player's max HP through mboss/pl_dot (no dodge, no parry, no position check: the failed judge is the hit;
# #mbDotLethal 0: it never kills), the push ring in the same tick (pl_dot has no knockback), the impact effects and sound.
scoreboard players set #mbDotPct mb 500
scoreboard players set #mbDotEl mb 3
scoreboard players set #mbDotLethal mb 0
function rlk:mboss/pl_dot
function rlk:mboss/push/ring {r:25,to:30,kb:3}
execute positioned ~ ~0.1 ~ run function rlk:boss/scarlet/fx/p/dive_impact {r:30}
execute positioned ~ ~0.1 ~ rotated 0 -90 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_sw","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_swn","rlk_hr_sw_col"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,0.3f,6f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_path","minecraft:custom_model_data":{colors:[14857471]}}}}
execute positioned ~ ~0.1 ~ rotated 0 -90 run tp @e[type=minecraft:item_display,tag=rlk_hr_swn] ~ ~ ~ ~ ~
tag @e[type=minecraft:item_display,tag=rlk_hr_swn] remove rlk_hr_swn
execute positioned ~ ~ ~ run function rlk:boss/scarlet/fx/snd/fail_impact
