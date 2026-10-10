execute as @e[tag=rlk_cmline,distance=..8] if score @s cmId = #cid tmp at @s run function rlk:cm/ar/shoot
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 11
scoreboard players operation @s cmCd = #cmCd_ar tmp
tag @s remove rlk_cmch
function rlk:cm/swing
execute unless score #k107 snd matches 1 run function rlk:snd/f114
