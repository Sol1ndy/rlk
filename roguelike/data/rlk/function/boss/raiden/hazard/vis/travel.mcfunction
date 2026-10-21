# @s = travelling hazard, one tick before its launch: summon its cards at the start state; the display clock
# gives them their ONE interpolation (to the end state over F ticks) on the launch tick.
execute store result storage rlk:rd v.d int 1 run scoreboard players get @s rdHF
scoreboard players operation #rdR1 rd = @s rdHB
scoreboard players operation #rdR1 rd *= @s rdHF
scoreboard players operation #rdR1 rd /= #rdK1000 rd
scoreboard players operation #rdR1 rd += @s rdHA
execute store result storage rlk:rd v.tz0 float 0.001 run scoreboard players get @s rdHA
execute store result storage rlk:rd v.tz1 float 0.001 run scoreboard players get #rdR1 rd
execute if score @s rdHK matches 5 run function rlk:boss/raiden/hazard/vis/travel_sweep
execute if score @s rdHK matches 6 run function rlk:boss/raiden/hazard/vis/travel_slab
execute if score @s rdHK matches 7 run function rlk:boss/raiden/hazard/vis/travel_orb
scoreboard players operation @e[tag=rlk_rd_vown] rdVId = @s rdHId
tag @e[tag=rlk_rd_vown] remove rlk_rd_vown
