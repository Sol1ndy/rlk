# BLUE 청광 돌파 (p1.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:mboss/mv/face
function rlk:boss/scarlet/rig/play/blue
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/chest
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run particle minecraft:dust{color:[0.35,0.62,1.0],scale:1.6} ~ ~ ~ 0.6 0.8 0.6 0 36 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run particle minecraft:dust{color:[1.0,0.88,0.29],scale:1.6} ~ ~ ~ 0.5 0.05 0.5 0 10 force @a[tag=player]
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/flash_blue
