# @s = a flying orb, at it: one step toward its landing point (the marker with the same apL), 1 / #apq35R of the way
# left (it arrives on the tick before the landing), the double-helix trail facing the flight.
scoreboard players operation #apq35K mb = @s apL
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p35d] if score @s apL = #apq35K mb run tag @s add rlk_mb_ap_p35t
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p35t,limit=1] feet run function rlk:boss/apep/fx/p/helix_trail
execute store result score #apq35X mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_ap_p35t,limit=1] Pos[0] 1000
execute store result score #apq35Y mb run data get entity @s Pos[0] 1000
scoreboard players operation #apq35X mb -= #apq35Y mb
scoreboard players operation #apq35X mb /= #apq35R mb
scoreboard players operation #apq35Y mb += #apq35X mb
execute store result entity @s Pos[0] double 0.001 run scoreboard players get #apq35Y mb
execute store result score #apq35X mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_ap_p35t,limit=1] Pos[1] 1000
scoreboard players add #apq35X mb 400
execute store result score #apq35Y mb run data get entity @s Pos[1] 1000
scoreboard players operation #apq35X mb -= #apq35Y mb
scoreboard players operation #apq35X mb /= #apq35R mb
scoreboard players operation #apq35Y mb += #apq35X mb
execute store result entity @s Pos[1] double 0.001 run scoreboard players get #apq35Y mb
execute store result score #apq35X mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_ap_p35t,limit=1] Pos[2] 1000
execute store result score #apq35Y mb run data get entity @s Pos[2] 1000
scoreboard players operation #apq35X mb -= #apq35Y mb
scoreboard players operation #apq35X mb /= #apq35R mb
scoreboard players operation #apq35Y mb += #apq35X mb
execute store result entity @s Pos[2] double 0.001 run scoreboard players get #apq35Y mb
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p35t] remove rlk_mb_ap_p35t
