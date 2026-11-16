# @s = hazard at its origin (rotated as it). The B.3 decal, sized to the hazard; rings open with an expand.
data modify storage rlk:rd v set value {tz:0f,d:1}
execute if score @s rdHDk matches 1 run function rlk:boss/raiden/hazard/vis/dk/1
execute if score @s rdHDk matches 2 run function rlk:boss/raiden/hazard/vis/dk/2
execute if score @s rdHDk matches 3 run function rlk:boss/raiden/hazard/vis/dk/3
execute if score @s rdHDk matches 4 run function rlk:boss/raiden/hazard/vis/dk/4
execute if score @s rdHDk matches 5 run function rlk:boss/raiden/hazard/vis/dk/5
execute if score @s rdHDk matches 6 run function rlk:boss/raiden/hazard/vis/dk/6
execute if score @s rdHDk matches 7 run function rlk:boss/raiden/hazard/vis/dk/7
execute if score @s rdHDk matches 8 run function rlk:boss/raiden/hazard/vis/dk/8
# radius: annulus = r (B); every other radial kind = A. band: width 2B x length A (rect / to_wall), offset C.
scoreboard players operation #rdSx rd = @s rdHA
execute if score @s rdHK matches 2 run scoreboard players operation #rdSx rd = @s rdHB
scoreboard players operation #rdSz rd = #rdSx rd
execute if score @s rdHDk matches 5 run function rlk:boss/raiden/hazard/vis/decal_band
execute store result storage rlk:rd v.sx float 0.001 run scoreboard players get #rdSx rd
execute store result storage rlk:rd v.sz float 0.001 run scoreboard players get #rdSz rd
execute store result storage rlk:rd v.sx0 float 0.001 run scoreboard players get #rdSx rd
execute store result storage rlk:rd v.sz0 float 0.001 run scoreboard players get #rdSz rd
execute if score @s rdHDk matches 1 store result storage rlk:rd v.sx0 float 0.00025 run scoreboard players get #rdSx rd
execute if score @s rdHDk matches 2 store result storage rlk:rd v.sx0 float 0.00025 run scoreboard players get #rdSx rd
execute if score @s rdHDk matches 3 store result storage rlk:rd v.sx0 float 0.00025 run scoreboard players get #rdSx rd
execute if score @s rdHDk matches 8 store result storage rlk:rd v.sx0 float 0.00025 run scoreboard players get #rdSx rd
execute if score @s rdHDk matches 1 store result storage rlk:rd v.sz0 float 0.00025 run scoreboard players get #rdSz rd
execute if score @s rdHDk matches 2 store result storage rlk:rd v.sz0 float 0.00025 run scoreboard players get #rdSz rd
execute if score @s rdHDk matches 3 store result storage rlk:rd v.sz0 float 0.00025 run scoreboard players get #rdSz rd
execute if score @s rdHDk matches 8 store result storage rlk:rd v.sz0 float 0.00025 run scoreboard players get #rdSz rd
function rlk:boss/raiden/hazard/vis/decal_summon with storage rlk:rd v
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
scoreboard players operation @e[tag=rlk_rd_vnew,limit=1] rdVId = @s rdHId
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
