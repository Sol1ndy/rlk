# Macro {tell}: the landing disc here in the volleys' group (quiet: none row).
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players operation #hzGrp mb = #apq35G mb
$function rlk:mboss/hz/disc {r:20,tell:$(tell),dmg:48}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p35h
