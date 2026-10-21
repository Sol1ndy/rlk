scoreboard players operation #rdSx rd = @s rdHC
scoreboard players operation #rdSx rd += @s rdHC
execute store result storage rlk:rd v.sx float 0.001 run scoreboard players get #rdSx rd
execute store result storage rlk:rd v.sy float 0.001 run scoreboard players get @s rdHE
execute store result storage rlk:rd v.sz float 0.001 run scoreboard players get @s rdHD
function rlk:boss/raiden/hazard/vis/slab_summon with storage rlk:rd v
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
tag @e[tag=rlk_rd_vnew,limit=1] add rlk_rd_vown
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
