# A4 사형장으로의 초대 (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt kn.
scoreboard players set #done kn 0
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig_stub/play/a4
execute at @s run playsound minecraft:entity.player.attack.nodamage hostile @a[tag=player] ~ ~ ~ 0.4 0.6 0.13
