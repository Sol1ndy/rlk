# MX 자광 십자참 (p_ghost.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:mboss/mv/face
scoreboard players set #mx_pre hr 0
execute at @s if entity @e[tag=rlk_body,limit=1,distance=..6] run return run function rlk:boss/scarlet/p/mx/retreat
function rlk:boss/scarlet/rig/play/mx
