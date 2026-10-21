# @s = hazard at its origin. The strike visual of a static hazard, sized to it (life 10: flash, flicker,
# residue, fade). Field crackle stays bound to the hazard instead.
data modify storage rlk:rd v set value {tz:0f,d:1}
execute if score @s rdHSv matches 1 run function rlk:boss/raiden/hazard/vis/sv/1
execute if score @s rdHSv matches 2 run function rlk:boss/raiden/hazard/vis/sv/2
execute if score @s rdHSv matches 3 run function rlk:boss/raiden/hazard/vis/sv/3
execute if score @s rdHSv matches 4 run function rlk:boss/raiden/hazard/vis/sv/4
execute if score @s rdHSv matches 5 run function rlk:boss/raiden/hazard/vis/sv/5
execute if score @s rdHSv matches 6 run function rlk:boss/raiden/hazard/vis/sv/6
execute if score @s rdHSv matches 7 run function rlk:boss/raiden/hazard/vis/sv/7
execute if score @s rdHSv matches 8 run function rlk:boss/raiden/hazard/vis/sv/8
execute if score @s rdHSv matches 9 run function rlk:boss/raiden/hazard/vis/sv/9
execute if score @s rdHSv matches 10 run function rlk:boss/raiden/hazard/vis/sv/10
scoreboard players operation #rdSx rd = @s rdHA
execute if score @s rdHK matches 2 run scoreboard players operation #rdSx rd = @s rdHB
scoreboard players operation #rdSz rd = #rdSx rd
execute if score @s rdHK matches 3..4 run function rlk:boss/raiden/hazard/vis/decal_band
execute store result storage rlk:rd v.sx float 0.001 run scoreboard players get #rdSx rd
execute store result storage rlk:rd v.sz float 0.001 run scoreboard players get #rdSz rd
execute store result storage rlk:rd v.sx0 float 0.00075 run scoreboard players get #rdSx rd
execute store result storage rlk:rd v.sz0 float 0.00075 run scoreboard players get #rdSz rd
execute if score @s rdHK matches 3..4 run function rlk:boss/raiden/hazard/vis/strike_full
execute if score @s rdHK matches 9 run function rlk:boss/raiden/hazard/vis/field_summon with storage rlk:rd v
execute unless score @s rdHK matches 9 run function rlk:boss/raiden/hazard/vis/strike_summon with storage rlk:rd v
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHLife 10
scoreboard players operation @e[tag=rlk_rd_vnew,limit=1] rdVId = @s rdHId
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
