# @s = crescent 3, at it (module tick: before mv and pj move it). Age = mbT; the flame puff trail every 2 t.
scoreboard players add @s mbT 1
scoreboard players operation #bfM mb = @s mbT
scoreboard players operation #bfM mb %= #bfK2 mb
execute if score #bfM mb matches 0 run function rlk:mboss/butterfly/fx/p/fire_trail
# age 5: the dive onto its marker (curved, 7 t; the prop lands 0.65 b up, the pj sub-step lifts it
# 0.25 b, so the hit point 0.9 b under it is on the floor at the marker)
execute if score @s mbT matches 5 at @e[type=minecraft:marker,tag=rlk_mb_bf_p12t3,limit=1] positioned ~ ~0.65 ~ run function rlk:mboss/mv/leap {t:7,h:8}
execute if score @s mbT matches 12 run function rlk:mboss/butterfly/p/barrage/land3
