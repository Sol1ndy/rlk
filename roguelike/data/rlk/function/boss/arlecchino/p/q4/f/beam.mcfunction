# Q4 the beam (@s = body): from the chest anchor through the lock, the burst at the lock, embers along the line.
kill @e[type=minecraft:marker,tag=rlk_kn_q4c]
function rlk:boss/arlecchino/p/q4/f/chest
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:boss/arlecchino/p/q4/f/dist3
execute store result storage rlk:kn p2.beam.len int 1 run scoreboard players get #q4_r kn
execute at @e[type=minecraft:marker,tag=rlk_kn_q4c,limit=1] facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet run function rlk:boss/arlecchino/fx/p/beam with storage rlk:kn p2.beam
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^2 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^5 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^8 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^11 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^14 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^17 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^20 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^23 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^26 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201.1 ~ positioned ^ ^ ^29 run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.05 0.6 0.01 3 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201.2 ~ run function rlk:boss/arlecchino/fx/p/impact_burst {r:22,c:2}
execute at @s run function rlk:boss/arlecchino/fx/snd/beam_fire
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:boss/arlecchino/fx/snd/impact
kill @e[type=minecraft:marker,tag=rlk_kn_q4c]
