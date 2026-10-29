# G2 gauge from a player hit (on_hit, @s = body inside combat/apply: scores only). Any reaction triggered on her -12;
# an electro-charged / burning tick -4; any other hit -1 (once per 5 t).
execute if score #rx tmp matches 1.. run return run scoreboard players remove #sh tk 12
execute if score #tfm tmp matches 1 if score #elem tmp matches 3 if score @s ecI matches 0 if score @s aWater matches 1.. run return run scoreboard players remove #sh tk 4
execute if score #tfm tmp matches 1 if score #elem tmp matches 1 if score @s burnOn matches 1 if score @s burnI matches 0 run return run scoreboard players remove #sh tk 4
execute if score #shicd tk matches 1.. run return 0
scoreboard players remove #sh tk 1
scoreboard players set #shicd tk 5
