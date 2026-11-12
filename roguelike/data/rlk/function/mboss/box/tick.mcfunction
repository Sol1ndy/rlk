# @s = box display, at @s. mbT = the box's own clock.
scoreboard players set #mbBoxOn mb 1
scoreboard players add @s mbT 1
execute if entity @s[tag=rlk_mb_boxfall] run return run function rlk:mboss/box/fall
execute if score @s mbT matches 10.. run function rlk:mboss/box/shimmer
