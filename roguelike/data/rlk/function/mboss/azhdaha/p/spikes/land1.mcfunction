# At point 2 (t37): the landing ring (kept decal, Change note 1) + its hazard, one group.
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #aq4G mb
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/disc {r:16,tell:14,dmg:34}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p4h
data modify storage rlk:mboss az.tl set value {r:16,tell:14,nd:0,hold:3}
execute store result storage rlk:mboss az.tl.el int 1 run scoreboard players get #azE mb
function rlk:mboss/azhdaha/fx/tele/crack_o with storage rlk:mboss az.tl
