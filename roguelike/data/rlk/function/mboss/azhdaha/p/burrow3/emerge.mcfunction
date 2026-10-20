# The emergence decal and burst at the centre: disc r 5.2, tell 28,
# the leg element + brand, dodgeable (step away from the surfacing spot).
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/disc {r:52,tell:28,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p23e
data modify storage rlk:mboss az.tl set value {r:52,tell:28,nd:0,hold:4}
execute store result storage rlk:mboss az.tl.el int 1 run scoreboard players get #azE mb
function rlk:mboss/azhdaha/kstub/tele/disc
