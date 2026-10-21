execute at @s positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..18,limit=1] run return 0
scoreboard players add #apCl mb 1
execute if score #apCl mb matches 80.. run return 0
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~
function rlk:mboss/apep/u/clamp_burst1_s
