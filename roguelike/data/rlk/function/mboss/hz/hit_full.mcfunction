# Whole arena: hit unless the body centre is inside the safe circle (radius mbHzR0) of the origin.
execute if score @s mbHzR0 matches ..0 run return run function rlk:mboss/hz/hurt
execute unless entity @e[tag=rlk_body,distance=..30,limit=1] run return run function rlk:mboss/hz/hurt
execute store result score #dx mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #dz mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
execute store result score #t mb run data get entity @s Pos[0] 1000
scoreboard players operation #dx mb -= #t mb
execute store result score #t mb run data get entity @s Pos[2] 1000
scoreboard players operation #dz mb -= #t mb
scoreboard players operation #r2 mb = #dx mb
scoreboard players operation #r2 mb *= #dx mb
scoreboard players operation #t mb = #dz mb
scoreboard players operation #t mb *= #dz mb
scoreboard players operation #r2 mb += #t mb
execute if score #r2 mb > @s mbHzRI run function rlk:mboss/hz/hurt
