execute if score #pOK mb matches 0 run return 0
execute store result score #t mb run data get entity @s Pos[0] 1000
scoreboard players operation #qx mb = #peX mb
scoreboard players operation #qx mb -= #t mb
execute store result score #t mb run data get entity @s Pos[2] 1000
scoreboard players operation #qz mb = #peZ mb
scoreboard players operation #qz mb -= #t mb
execute unless score #qx mb matches -48000..48000 run return 0
execute unless score #qz mb matches -48000..48000 run return 0
scoreboard players operation #q2 mb = #qx mb
scoreboard players operation #q2 mb *= @s mbHzFX
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= @s mbHzFZ
scoreboard players operation #q2 mb += #t mb
scoreboard players operation #q2 mb /= #c1000 mb
execute if score #q2 mb < @s mbHzLo run return 0
execute if score #q2 mb > @s mbHzHi run return 0
scoreboard players operation #qs mb = #qx mb
scoreboard players operation #qs mb *= @s mbHzFZ
scoreboard players operation #t mb = #qz mb
scoreboard players operation #t mb *= @s mbHzFX
scoreboard players operation #qs mb -= #t mb
scoreboard players operation #qs mb /= #c1000 mb
execute if score #qs mb matches ..-1 run scoreboard players operation #qs mb *= #cm1 mb
execute if score #qs mb <= @s mbHzHW run scoreboard players set #pOK mb 0
