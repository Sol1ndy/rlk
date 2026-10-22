# @s = the player: #apq32P = the horizontal distance to the arena centre in tenths.
execute store result score #apq32Dx mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] Pos[0] 10
execute store result score #apq32X mb run data get entity @s Pos[0] 10
scoreboard players operation #apq32Dx mb -= #apq32X mb
execute store result score #apq32Dz mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] Pos[2] 10
execute store result score #apq32X mb run data get entity @s Pos[2] 10
scoreboard players operation #apq32Dz mb -= #apq32X mb
scoreboard players operation #apq32N mb = #apq32Dx mb
scoreboard players operation #apq32N mb *= #apq32Dx mb
scoreboard players operation #apq32X mb = #apq32Dz mb
scoreboard players operation #apq32X mb *= #apq32Dz mb
scoreboard players operation #apq32N mb += #apq32X mb
scoreboard players set #apq32P mb 0
execute if score #apq32N mb matches ..0 run return 0
scoreboard players set #apq32P mb 300
scoreboard players operation #apq32X mb = #apq32N mb
scoreboard players operation #apq32X mb /= #apq32P mb
scoreboard players operation #apq32P mb += #apq32X mb
scoreboard players operation #apq32P mb /= #c2 mb
execute if score #apq32P mb matches ..0 run scoreboard players set #apq32P mb 1
scoreboard players operation #apq32X mb = #apq32N mb
scoreboard players operation #apq32X mb /= #apq32P mb
scoreboard players operation #apq32P mb += #apq32X mb
scoreboard players operation #apq32P mb /= #c2 mb
execute if score #apq32P mb matches ..0 run scoreboard players set #apq32P mb 1
scoreboard players operation #apq32X mb = #apq32N mb
scoreboard players operation #apq32X mb /= #apq32P mb
scoreboard players operation #apq32P mb += #apq32X mb
scoreboard players operation #apq32P mb /= #c2 mb
execute if score #apq32P mb matches ..0 run scoreboard players set #apq32P mb 1
scoreboard players operation #apq32X mb = #apq32N mb
scoreboard players operation #apq32X mb /= #apq32P mb
scoreboard players operation #apq32P mb += #apq32X mb
scoreboard players operation #apq32P mb /= #c2 mb
execute if score #apq32P mb matches ..0 run scoreboard players set #apq32P mb 1
scoreboard players operation #apq32X mb = #apq32N mb
scoreboard players operation #apq32X mb /= #apq32P mb
scoreboard players operation #apq32P mb += #apq32X mb
scoreboard players operation #apq32P mb /= #c2 mb
execute if score #apq32P mb matches ..0 run scoreboard players set #apq32P mb 1
scoreboard players operation #apq32X mb = #apq32N mb
scoreboard players operation #apq32X mb /= #apq32P mb
scoreboard players operation #apq32P mb += #apq32X mb
scoreboard players operation #apq32P mb /= #c2 mb
execute if score #apq32P mb matches ..0 run scoreboard players set #apq32P mb 1
scoreboard players operation #apq32X mb = #apq32N mb
scoreboard players operation #apq32X mb /= #apq32P mb
scoreboard players operation #apq32P mb += #apq32X mb
scoreboard players operation #apq32P mb /= #c2 mb
execute if score #apq32P mb matches ..0 run scoreboard players set #apq32P mb 1
