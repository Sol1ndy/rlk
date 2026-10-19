execute if score #pOK mb matches 0 run return 0
execute store result score #t mb run data get entity @s Pos[0] 1000
scoreboard players operation #qx mb = #peX mb
scoreboard players operation #qx mb -= #t mb
execute store result score #t mb run data get entity @s Pos[2] 1000
scoreboard players operation #qz mb = #peZ mb
scoreboard players operation #qz mb -= #t mb
execute unless score #qx mb matches -32000..32000 run return 0
execute unless score #qz mb matches -32000..32000 run return 0
scoreboard players operation #q2 mb = #qx mb
scoreboard players operation #q2 mb *= #qx mb
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= #qz mb
scoreboard players operation #q2 mb += #t mb
execute if score #q2 mb <= @s mbHzRR if score #q2 mb >= @s mbHzRI run scoreboard players set #pOK mb 0
