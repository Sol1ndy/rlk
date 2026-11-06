# @s = crescent 3 of swing 1, at it (module tick: before mv and pj move it). Age = mbT; its flame tail.
scoreboard players add @s mbT 1
# the flame tail while it flies (its helper rlk_mb_bf_p12q13 holds last tick's spot; gone with the landing)
execute if entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12q13,limit=1] run function rlk:mboss/butterfly/p/barrage/tail13
scoreboard players operation #bfM mb = @s mbT
scoreboard players operation #bfM mb %= #bfK4 mb
execute if score #bfM mb matches 0 run particle minecraft:small_flame ~ ~ ~ 0.08 0.08 0.08 0.01 2 force @a[tag=player]
# age 5: the dive onto its marker (curved, D t; the prop lands 0.65 b up, the pj sub-step lifts it 0.25 b,
# so the hit point 0.9 b under it is on the floor at the marker)
execute if score @s mbT matches 5 at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t13,limit=1] positioned ~ ~0.65 ~ run function rlk:mboss/mv/leap {t:7,h:4}
execute if score @s mbT matches 5 run scoreboard players operation @s mbMvN = @s mbS
execute if score @s mbT matches 5 run scoreboard players remove @s mbMvN 5
execute if score @s mbT = @s mbS run function rlk:mboss/butterfly/p/barrage/land13
