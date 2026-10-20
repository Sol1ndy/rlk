# @s = body: one run tick: 1 b forward along the locked line while the next anchor stays inside r 12
# of the arena centre, at most 24 ticks; dust + gallop every 4 t; no body push.
scoreboard players set #azNoPush mb 1
scoreboard players add #aq3N mb 1
scoreboard players set #aq3M mb 0
execute store success score #aq3M mb at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..12,limit=1] run tp @s ~ ~ ~
execute if score #aq3M mb matches 0 run return run function rlk:mboss/azhdaha/p/charge/stop
scoreboard players operation #azM mb = #aq3N mb
scoreboard players operation #azM mb %= #azK4 mb
execute if score #azM mb matches 1 at @s run function rlk:mboss/azhdaha/fx/snd/charge_gallop
execute if score #azM mb matches 1 at @s run function rlk:mboss/azhdaha/fx/p/dust_trail
execute if score #aq3N mb matches 24.. run return run function rlk:mboss/azhdaha/p/charge/stop
