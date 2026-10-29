# B1 날개 가리기 2연격 (S3, p_melee.py): pattern tick 0 (@s = the body, at it). Clock #pt tk.
scoreboard players set #done tk 0
function rlk:mboss/mv/face
function rlk:boss/tachy/rig_stub/play/b1_wrap2
playsound minecraft:entity.iron_golem.step hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
