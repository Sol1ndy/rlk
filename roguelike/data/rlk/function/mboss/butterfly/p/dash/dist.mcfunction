# @s = body: #bp3D = the lane bucket of |S D| (0.5 b steps from 1.0 b; -1 below 0.75 b).
execute store result score #bp3X mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] Pos[0] 10
execute store result score #t mb run data get entity @s Pos[0] 10
scoreboard players operation #bp3X mb -= #t mb
execute store result score #bp3Z mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] Pos[2] 10
execute store result score #t mb run data get entity @s Pos[2] 10
scoreboard players operation #bp3Z mb -= #t mb
scoreboard players operation #bp3X mb *= #bp3X mb
scoreboard players operation #bp3Z mb *= #bp3Z mb
scoreboard players operation #bp3X mb += #bp3Z mb
scoreboard players set #bp3D mb -1
execute if score #bp3X mb matches 57..156 run scoreboard players set #bp3D mb 0
execute if score #bp3X mb matches 157..306 run scoreboard players set #bp3D mb 1
execute if score #bp3X mb matches 307..506 run scoreboard players set #bp3D mb 2
execute if score #bp3X mb matches 507..756 run scoreboard players set #bp3D mb 3
execute if score #bp3X mb matches 757..1056 run scoreboard players set #bp3D mb 4
execute if score #bp3X mb matches 1057..1406 run scoreboard players set #bp3D mb 5
execute if score #bp3X mb matches 1407..1806 run scoreboard players set #bp3D mb 6
execute if score #bp3X mb matches 1807..2256 run scoreboard players set #bp3D mb 7
execute if score #bp3X mb matches 2257..2756 run scoreboard players set #bp3D mb 8
execute if score #bp3X mb matches 2757..3306 run scoreboard players set #bp3D mb 9
execute if score #bp3X mb matches 3307..3906 run scoreboard players set #bp3D mb 10
execute if score #bp3X mb matches 3907..4556 run scoreboard players set #bp3D mb 11
execute if score #bp3X mb matches 4557.. run scoreboard players set #bp3D mb 12
