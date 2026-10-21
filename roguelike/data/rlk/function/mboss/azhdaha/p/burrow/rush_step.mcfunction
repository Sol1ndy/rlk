# @s = body (hidden): 0.6 b/t along the lane (inside the arena), the rush disc rides the body;
# the travelling mound: earth thrown up over the body every tick (vanilla particles, no fx cards)
execute at @s positioned ^ ^ ^0.6 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute at @s as @e[type=minecraft:marker,tag=rlk_mb_az_p9rush] run tp @s ~ ~ ~
execute at @s run particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.3 ~ 1.1 0.25 1.1 0.15 14 force @a[tag=player]
execute at @s run particle minecraft:block{block_state:"minecraft:tuff"} ~ ~0.2 ~ 0.9 0.2 0.9 0.1 8 force @a[tag=player]
# (FIX STATE-2 / STATE-14) the dust trail every other tick (3 cards each, life 14)
scoreboard players operation #aq9Q mb = #azPT mb
scoreboard players operation #aq9Q mb %= #c2 mb
execute if score #aq9Q mb matches 0 at @s run function rlk:mboss/azhdaha/fx/p/dust
