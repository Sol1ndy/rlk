scoreboard players set @s cmS 0
scoreboard players set @s cmAR 8
execute as @e[tag=rlk_ns_katana,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b}
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^1.1 ^1.1 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1 normal
execute unless score #c2nsslash snd matches 1 run function rlk:cm/c2/snd/nsslash
execute if score #c2NsHit tmp matches 0 if entity @e[tag=rlk_body,distance=..3.0] run function rlk:cm/ns/hit
