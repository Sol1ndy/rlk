summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_dome"]}
scoreboard players set @e[tag=rlk_rd_dome] rdTime 0
function rlk:boss/raiden/vfx/dome_create
playsound minecraft:block.beacon.activate player @a[tag=player] ~ ~ ~ .85 1.25 .4
