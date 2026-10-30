# Macro {tell}: the emergence burst at the centre with the given tell.
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
$function rlk:mboss/hz/disc {r:52,tell:$(tell),dmg:122}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p23e
