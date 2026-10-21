# @s = boss. Abort the running attack (same reset as a pause), then enter the right phase.
execute unless score @s rdPat matches 0 run function rlk:boss/raiden/pause
execute if score #rdReq rd matches 11..18 if score @s rdPhase matches 0 run function rlk:boss/raiden/transform_start
execute if score #rdReq rd matches 11..18 if score @s rdPhase matches 3 run function rlk:boss/raiden/transform_start
execute if score #rdReq rd matches 1..10 if score @s rdPhase matches 1.. run function rlk:boss/raiden/test/to_normal
execute if score #rdReq rd matches 21..28 if score @s rdPhase matches 1.. run function rlk:boss/raiden/test/to_normal
scoreboard players set @s rdWalk 0
execute unless score @s rdPhase matches 1 run scoreboard players set @s rdCool 2
