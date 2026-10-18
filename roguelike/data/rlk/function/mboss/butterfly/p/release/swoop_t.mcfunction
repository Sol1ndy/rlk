# @s = body at clock 0: #bp15T = the swoop time to R, ceil(|SR| / 1.0 b/t) clamped to 9..13 (|SR| squared in tenths; fix F3).
execute store result score #bp15X mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] Pos[0] 10
execute store result score #t mb run data get entity @s Pos[0] 10
scoreboard players operation #bp15X mb -= #t mb
execute store result score #bp15Z mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] Pos[2] 10
execute store result score #t mb run data get entity @s Pos[2] 10
scoreboard players operation #bp15Z mb -= #t mb
scoreboard players operation #bp15X mb *= #bp15X mb
scoreboard players operation #bp15Z mb *= #bp15Z mb
scoreboard players operation #bp15X mb += #bp15Z mb
scoreboard players set #bp15T mb 9
execute if score #bp15X mb matches 8101.. run scoreboard players set #bp15T mb 10
execute if score #bp15X mb matches 10001.. run scoreboard players set #bp15T mb 11
execute if score #bp15X mb matches 12101.. run scoreboard players set #bp15T mb 12
execute if score #bp15X mb matches 14401.. run scoreboard players set #bp15T mb 13
