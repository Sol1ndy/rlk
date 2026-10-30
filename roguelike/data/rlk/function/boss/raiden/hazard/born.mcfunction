# Common creation tail (as the creator): age -1 so the world tick that follows makes it 0 this tick.
tag @e[tag=rlk_rd_hnew,limit=1] add rlk_rd_hazard
scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHAge -1
scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHHit 0
scoreboard players set @e[tag=rlk_rd_hnew,limit=1] mlv 1
execute if entity @e[tag=rlk_raiden,limit=1] run scoreboard players operation @e[tag=rlk_rd_hnew,limit=1] mlv = @e[tag=rlk_raiden,limit=1] mlv
execute as @e[tag=rlk_rd_hnew,limit=1] at @s rotated as @s run function rlk:boss/raiden/hazard/init
tag @e[tag=rlk_rd_hnew] remove rlk_rd_hnew
