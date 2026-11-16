# @s = a linked basic; at the 양육 orb, rotated toward it: len ~ the horizontal distance (octagon estimate) + the drop.
execute store result score #apDX mb run data get entity @s Pos[0] 10
execute store result score #apDZ mb run data get entity @s Pos[2] 10
scoreboard players operation #apDX mb -= #apNX mb
scoreboard players operation #apDZ mb -= #apNZ mb
execute if score #apDX mb matches ..-1 run scoreboard players operation #apDX mb *= #apM1 mb
execute if score #apDZ mb matches ..-1 run scoreboard players operation #apDZ mb *= #apM1 mb
scoreboard players operation #apLn mb = #apDX mb
scoreboard players operation #apLn mb > #apDZ mb
scoreboard players operation #apDX mb < #apDZ mb
scoreboard players operation #apDX mb *= #c2 mb
scoreboard players operation #apDX mb /= #apC5 mb
scoreboard players operation #apLn mb += #apDX mb
scoreboard players add #apLn mb 8
execute store result storage rlk:mboss ap.o.len int 1 run scoreboard players get #apLn mb
function rlk:boss/apep/fx/p/tether with storage rlk:mboss ap.o
