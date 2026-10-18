# @s = a blade prop, at and rotated as it (0.9 b over the floor), before the framework moves it this tick
# (core ai/state, so its age mbPjT = pattern clock - 17: the trail from 18, every 2 t).
scoreboard players add #bp4B mb 1
particle minecraft:dust{color:[0.392f,0.737f,0.337f],scale:1.4} ^ ^-0.85 ^ 1.3 0.2 0.1 0 3 force @a[tag=player]
particle minecraft:dust_color_transition{from_color:[0.965f,0.992f,0.878f],to_color:[0.392f,0.737f,0.337f],scale:1} ^ ^2.9 ^ 1 0.2 0.1 0 2 force @a[tag=player]
scoreboard players operation #bfM mb = @s mbPjT
scoreboard players operation #bfM mb %= #bfK2 mb
execute if score #bfM mb matches 1 positioned ^ ^-0.9 ^ run function rlk:mboss/butterfly/fx/p/vac_trail
scoreboard players operation #bfM mb = @s mbPjT
scoreboard players operation #bfM mb %= #bfK4 mb
execute if score #bfM mb matches 1 run function rlk:mboss/butterfly/p/vacuum/debris
execute if score @s mbPjT matches 6 run playsound minecraft:entity.breeze.idle_air hostile @a[tag=player] ~ ~ ~ 0.4 1 0.13
execute unless entity @s[tag=rlk_mb_bf_p4s] if entity @e[tag=rlk_body,distance=..4,limit=1] run function rlk:mboss/butterfly/p/vacuum/pass
