# #mbDist mb = horizontal distance @s -> player body in tenths of a block (integer Newton square root).
execute store result score #dx mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 10
execute store result score #t mb run data get entity @s Pos[0] 10
scoreboard players operation #dx mb -= #t mb
execute store result score #dz mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 10
execute store result score #t mb run data get entity @s Pos[2] 10
scoreboard players operation #dz mb -= #t mb
scoreboard players operation #n mb = #dx mb
scoreboard players operation #n mb *= #dx mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #dz mb
scoreboard players operation #n mb += #t mb
scoreboard players set #mbDist mb 0
execute if score #n mb matches ..0 run return 0
execute if score #n mb matches 4000001.. run return run scoreboard players set #mbDist mb 2000
scoreboard players set #mbDist mb 2000
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
scoreboard players operation #t mb = #n mb
scoreboard players operation #t mb /= #mbDist mb
scoreboard players operation #mbDist mb += #t mb
scoreboard players operation #mbDist mb /= #c2 mb
execute if score #mbDist mb matches ..0 run scoreboard players set #mbDist mb 1
