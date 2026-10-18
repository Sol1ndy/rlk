# @s = a missile, at it: rise (1), turnover lock + decal + dive (7), impact (20).
scoreboard players add @s mbT 1
execute if score @s mbT matches 1 rotated as @s run tp @s ^ ^11 ^3
execute if score @s mbT matches 7 run function rlk:mboss/fieldgen/p/missile/lock
execute if score @s mbT matches 20.. run function rlk:mboss/fieldgen/p/missile/impact
