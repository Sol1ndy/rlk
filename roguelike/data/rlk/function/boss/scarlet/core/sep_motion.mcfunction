# @s = the body; the avatar entity (rlk_av) #bx_d mb from her: its Motion (b/t x 10000) loses the pull toward her beyond what
# leaves it 1.4 b off after this tick's physics (the walk view/move set; vanilla moves it by Motion after the functions).
execute store result score #bx_mx hr run data get entity @e[tag=rlk_av,limit=1] Motion[0] 10000
execute store result score #bx_mz hr run data get entity @e[tag=rlk_av,limit=1] Motion[2] 10000
scoreboard players operation #bx_in hr = #bx_mx hr
scoreboard players operation #bx_in hr *= #bx_ux hr
scoreboard players operation #bx_k hr = #bx_mz hr
scoreboard players operation #bx_k hr *= #bx_uz hr
scoreboard players operation #bx_in hr += #bx_k hr
scoreboard players operation #bx_in hr /= #cn1000 hr
scoreboard players operation #bx_al hr = #bx_d hr
scoreboard players remove #bx_al hr 1410
scoreboard players operation #bx_al hr *= #c10 hr
execute if score #bx_al hr matches ..-1 run scoreboard players set #bx_al hr 0
execute if score #bx_in hr <= #bx_al hr run return 0
scoreboard players operation #bx_in hr -= #bx_al hr
scoreboard players operation #bx_k hr = #bx_ux hr
scoreboard players operation #bx_k hr *= #bx_in hr
scoreboard players operation #bx_k hr /= #c1000 hr
scoreboard players operation #bx_mx hr += #bx_k hr
scoreboard players operation #bx_k hr = #bx_uz hr
scoreboard players operation #bx_k hr *= #bx_in hr
scoreboard players operation #bx_k hr /= #c1000 hr
scoreboard players operation #bx_mz hr += #bx_k hr
execute store result entity @e[tag=rlk_av,limit=1] Motion[0] double 0.0001 run scoreboard players get #bx_mx hr
execute store result entity @e[tag=rlk_av,limit=1] Motion[2] double 0.0001 run scoreboard players get #bx_mz hr
