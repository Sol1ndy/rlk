# @s = the body (cancel): glide stopped, on the floor below her (walked inside mv/ok by u/fit; the arena centre
# if none passed), visible, vulnerable.
execute if entity @s[tag=rlk_mb_mv] run function rlk:mboss/mv/stop
tag @s remove rlk_mb_inv
kill @e[type=minecraft:marker,tag=rlk_tk_w1set]
execute at @s positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_w1","rlk_tk_air","rlk_tk_w1set"]}
scoreboard players set #w1_n tk 0
execute as @e[type=minecraft:marker,tag=rlk_tk_w1set,limit=1] run function rlk:boss/tachy/p/w1/u/fit
execute store success score #w1_n tk at @e[type=minecraft:marker,tag=rlk_tk_w1set,limit=1] if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #w1_n tk matches 0 run function rlk:mboss/mv/home
kill @e[type=minecraft:marker,tag=rlk_tk_w1set]
function rlk:boss/tachy/rig/state/normal
function rlk:boss/tachy/el/edge
function rlk:boss/tachy/rig/look/chest/off
