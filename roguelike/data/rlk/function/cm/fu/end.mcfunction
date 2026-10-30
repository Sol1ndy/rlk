scoreboard players set @s cmS 0
scoreboard players set @s cmAR 8
execute as @e[tag=rlk_fu_glow,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b}
