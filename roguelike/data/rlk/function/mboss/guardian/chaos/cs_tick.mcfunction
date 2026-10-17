# @s = stream head (gold cube): out along its own heading for 10 t, then a spiralling dive at the player's feet.
scoreboard players add @s mbT 1
execute if score @s mbT matches 48.. run return run function rlk:mboss/guardian/chaos/cs_end
execute if score @s mbT matches 10.. at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute if score @s mbS matches 1 at @s run tp @s ^0.2 ^ ^0.45
execute if score @s mbS matches 2 at @s run tp @s ^-0.2 ^ ^0.45
particle minecraft:dust_color_transition{from_color:[0.99f,0.33f,0.33f],to_color:[0.3f,0.15f,0.13f],scale:1.5} ~ ~ ~ 0.06 0.06 0.06 0 2 force @a[tag=player]
scoreboard players operation #gdM mb = @s mbT
scoreboard players operation #gdM mb %= #gdK5 mb
execute if score #gdM mb matches 0 run particle minecraft:small_flame ~ ~ ~ 0.1 0.1 0.1 0.01 1 force @a[tag=player]
execute if score @s mbT matches 12.. at @s if entity @e[tag=rlk_body,distance=..1.4,limit=1] run return run function rlk:mboss/guardian/chaos/cs_end
execute at @s unless block ~ ~-0.3 ~ #rlk:cm_pass run function rlk:mboss/guardian/chaos/cs_end
