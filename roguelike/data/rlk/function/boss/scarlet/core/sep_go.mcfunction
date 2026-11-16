# @s = the body; #bx_d = the avatar's distance (mb), #bx_ux / #bx_uz the unit her -> the avatar (per mille).
scoreboard players operation #bx_p hr = #bx_d hr
scoreboard players set #bx_k hr 1410
scoreboard players operation #bx_k hr -= #bx_p hr
scoreboard players operation #bx_p hr = #bx_k hr
execute if score #bx_p hr matches 251.. run scoreboard players set #bx_p hr 250
scoreboard players operation #bx_k hr = #bx_ux hr
scoreboard players operation #bx_k hr *= #c5 hr
scoreboard players operation #bx_k hr /= #c100 hr
execute store result storage rlk:hr bx.x double 0.001 run scoreboard players get #bx_k hr
scoreboard players operation #bx_k hr = #bx_uz hr
scoreboard players operation #bx_k hr *= #c5 hr
scoreboard players operation #bx_k hr /= #c100 hr
execute store result storage rlk:hr bx.z double 0.001 run scoreboard players get #bx_k hr
execute if score #bx_p hr matches 1.. run function rlk:boss/scarlet/core/sep_step with storage rlk:hr bx
execute if entity @e[tag=rlk_av,limit=1] run function rlk:boss/scarlet/core/sep_motion
scoreboard players set #mbPlG mb -1
