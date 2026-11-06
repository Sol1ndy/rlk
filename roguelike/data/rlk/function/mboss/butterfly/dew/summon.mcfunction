# A glowing moon-dew orb 1.1 b above the floor here (an item_display dressed as the kit's dew look, with a lime
# glow outline; rlk_mb_aux: dies with the fight), the kit's spawn ripple and chime.
summon minecraft:item_display ~ ~1.1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_dew","rlk_mb_bf_dewn"],billboard:"center",Glowing:1b,glow_color_override:11985754,brightness:{block:15,sky:15},item:{id:"minecraft:slime_ball",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_dewn] run function rlk:mboss/butterfly/fx/prop/dew
# its age starts 7 t after the previous orb's, so the 20 t idle pulses never land on one tick (fix FX-2)
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_bf_dewn] mbT = #bfDewP mb
scoreboard players add #bfDewP mb 7
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_dewn] remove rlk_mb_bf_dewn
scoreboard players add #bfDewN mb 1
function rlk:mboss/butterfly/fx/p/dew_spawn
particle minecraft:end_rod ~ ~1.1 ~ 0.1 0.1 0.1 0.08 6 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/dew_spawn
