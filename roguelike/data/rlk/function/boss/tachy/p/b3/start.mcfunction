# B3 충전 6연격 (S3, p_melee.py): pattern tick 0 (@s = the body, at it). Clock #pt tk.
scoreboard players set #done tk 0
function rlk:mboss/mv/face
function rlk:boss/tachy/rig_stub/play/b3_six
function rlk:boss/tachy/rig_stub/look/chest/red
execute at @s run particle minecraft:dust{color:[1.0,0.25,0.1],scale:1.6} ~ ~1.5 ~ 0.2 0.2 0.2 0 8 force @a[tag=player]
playsound minecraft:entity.warden.sonic_charge hostile @a[tag=player] ~ ~ ~ 0.5 1.3 0.17
