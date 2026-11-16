# @s = body: #apq36D = the horizontal distance to L in tenths.
execute store result score #apq36Dx mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_ap_p36l,limit=1] Pos[0] 10
execute store result score #apq36X mb run data get entity @s Pos[0] 10
scoreboard players operation #apq36Dx mb -= #apq36X mb
execute store result score #apq36Dz mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_ap_p36l,limit=1] Pos[2] 10
execute store result score #apq36X mb run data get entity @s Pos[2] 10
scoreboard players operation #apq36Dz mb -= #apq36X mb
scoreboard players operation #apq36N mb = #apq36Dx mb
scoreboard players operation #apq36N mb *= #apq36Dx mb
scoreboard players operation #apq36X mb = #apq36Dz mb
scoreboard players operation #apq36X mb *= #apq36Dz mb
scoreboard players operation #apq36N mb += #apq36X mb
scoreboard players set #apq36D mb 0
execute if score #apq36N mb matches ..0 run return 0
scoreboard players set #apq36D mb 300
scoreboard players operation #apq36X mb = #apq36N mb
scoreboard players operation #apq36X mb /= #apq36D mb
scoreboard players operation #apq36D mb += #apq36X mb
scoreboard players operation #apq36D mb /= #c2 mb
execute if score #apq36D mb matches ..0 run scoreboard players set #apq36D mb 1
scoreboard players operation #apq36X mb = #apq36N mb
scoreboard players operation #apq36X mb /= #apq36D mb
scoreboard players operation #apq36D mb += #apq36X mb
scoreboard players operation #apq36D mb /= #c2 mb
execute if score #apq36D mb matches ..0 run scoreboard players set #apq36D mb 1
scoreboard players operation #apq36X mb = #apq36N mb
scoreboard players operation #apq36X mb /= #apq36D mb
scoreboard players operation #apq36D mb += #apq36X mb
scoreboard players operation #apq36D mb /= #c2 mb
execute if score #apq36D mb matches ..0 run scoreboard players set #apq36D mb 1
scoreboard players operation #apq36X mb = #apq36N mb
scoreboard players operation #apq36X mb /= #apq36D mb
scoreboard players operation #apq36D mb += #apq36X mb
scoreboard players operation #apq36D mb /= #c2 mb
execute if score #apq36D mb matches ..0 run scoreboard players set #apq36D mb 1
scoreboard players operation #apq36X mb = #apq36N mb
scoreboard players operation #apq36X mb /= #apq36D mb
scoreboard players operation #apq36D mb += #apq36X mb
scoreboard players operation #apq36D mb /= #c2 mb
execute if score #apq36D mb matches ..0 run scoreboard players set #apq36D mb 1
scoreboard players operation #apq36X mb = #apq36N mb
scoreboard players operation #apq36X mb /= #apq36D mb
scoreboard players operation #apq36D mb += #apq36X mb
scoreboard players operation #apq36D mb /= #c2 mb
execute if score #apq36D mb matches ..0 run scoreboard players set #apq36D mb 1
scoreboard players operation #apq36X mb = #apq36N mb
scoreboard players operation #apq36X mb /= #apq36D mb
scoreboard players operation #apq36D mb += #apq36X mb
scoreboard players operation #apq36D mb /= #c2 mb
execute if score #apq36D mb matches ..0 run scoreboard players set #apq36D mb 1
