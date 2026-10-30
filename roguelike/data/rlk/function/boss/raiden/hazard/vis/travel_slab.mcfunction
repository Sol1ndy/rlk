scoreboard players operation #rdSx rd = @s rdHC
scoreboard players operation #rdSx rd += @s rdHC
execute store result storage rlk:rd v.sx float 0.001 run scoreboard players get #rdSx rd
execute store result storage rlk:rd v.sy float 0.001 run scoreboard players get @s rdHE
execute store result storage rlk:rd v.sz float 0.001 run scoreboard players get @s rdHD
data modify storage rlk:rd v.m set value "tr_slab"
data modify storage rlk:rd v.ty set value 0f
data modify storage rlk:rd v.lr set value "[0f,0f,0f,1f]"
# rdHSv 2..4 (rd-sync): a crescent sword wave rolled 45 deg up to her left / right, or level, scaled to the half width
execute if score @s rdHSv matches 2.. run data modify storage rlk:rd v.m set value "tr_wave"
execute if score @s rdHSv matches 2.. run data modify storage rlk:rd v.ty set value 2.6f
execute if score @s rdHSv matches 2.. store result storage rlk:rd v.sx float 0.001080 run scoreboard players get @s rdHC
execute if score @s rdHSv matches 2.. run data modify storage rlk:rd v.sy set from storage rlk:rd v.sx
execute if score @s rdHSv matches 2.. run data modify storage rlk:rd v.sz set from storage rlk:rd v.sx
execute if score @s rdHSv matches 2 run data modify storage rlk:rd v.lr set value "[0f,0f,0.38268f,0.92388f]"
execute if score @s rdHSv matches 3 run data modify storage rlk:rd v.lr set value "[0f,0f,-0.38268f,0.92388f]"
function rlk:boss/raiden/hazard/vis/slab_summon with storage rlk:rd v
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
tag @e[tag=rlk_rd_vnew,limit=1] add rlk_rd_vown
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
