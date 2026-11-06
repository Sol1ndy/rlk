scoreboard players set @s cmS 0
scoreboard players set @s cmAR 16
tag @s remove rlk_cmch
execute as @e[tag=rlk_c3glow,tag=rlk_em_pt,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b}
