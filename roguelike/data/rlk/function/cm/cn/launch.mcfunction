execute as @e[tag=rlk_cmcbw,distance=..6] if score @s cmId = #cid tmp at @s run function rlk:cm/cn/go
scoreboard players set @s cmS 0
scoreboard players operation @s cmCd = #cmCd_cn tmp
scoreboard players set @s cmAR 10
tag @s remove rlk_cmch
function rlk:cm/swing
