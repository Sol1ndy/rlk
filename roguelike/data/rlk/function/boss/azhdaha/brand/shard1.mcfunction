# @s = a shard (module clock: frozen while paused): ages, sparkles, is picked up within 1.4 b.
scoreboard players remove @s azT 1
execute if score @s azT matches ..0 run return run kill @s
scoreboard players operation #azM mb = @s azT
scoreboard players operation #azM mb %= #azK4 mb
execute if score #azM mb matches 0 run particle minecraft:wax_on ~ ~0.3 ~ 0.15 0.15 0.15 0 1 force @a[tag=player]
execute if entity @a[tag=player,distance=..1.4,limit=1] run function rlk:boss/azhdaha/brand/shard_pick
