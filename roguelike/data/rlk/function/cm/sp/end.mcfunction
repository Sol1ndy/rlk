scoreboard players set @s cmS 0
scoreboard players set @s cmAR 12
tag @s remove rlk_cmch
execute as @e[tag=rlk_sp_yari,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b,brightness:{sky:0,block:0}}
