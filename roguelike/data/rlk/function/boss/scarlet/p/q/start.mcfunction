# Q 자영 포박 · 천공 낙월 (p_ghost.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:mboss/mv/face
scoreboard players set #q_hit hr 0
function rlk:boss/scarlet/rig/play/q_grab
function rlk:boss/scarlet/rig/anchor/blade_mid
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:1}
