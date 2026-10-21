# @s = a stalk root marker, facing the lock: step 0.5 b toward it while beyond r 25.3 (<= 8 steps).
execute positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..25.3,limit=1] run return 0
scoreboard players add #apq2N mb 1
execute if score #apq2N mb matches 9.. run return 0
tp @s ^ ^ ^0.5
function rlk:boss/apep/p/hands/root
