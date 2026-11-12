scoreboard players reset #k198 snd
scoreboard players set @s rcU 1
scoreboard players operation @s rvpLast = @s dgAt
scoreboard players operation #H_c0 rvp = @s dashCool
execute store result score #now cb run time query gametime
function rlk:player/def/input
execute if score @s rcT > #H_rcTmax rvp run scoreboard players operation #H_rcTmax rvp = @s rcT
execute if score #k198 snd matches 1 run scoreboard players add #H_fail rvp 1
execute unless score @s rvpLast = @s dgAt run scoreboard players add #H_dg rvp 1
execute if score @s dashCool matches 1.. run scoreboard players remove @s dashCool 1
scoreboard players add #k rvp 1
execute if score #k rvp matches 40.. run function rvp:a02_end
