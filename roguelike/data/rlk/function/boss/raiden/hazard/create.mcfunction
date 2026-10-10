# Called as the boss/aim marker at floor height. Pitch is flattened, yaw frozen.
summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_hazard","rlk_raiden_aux","rlk_room","rlk_rd_hnew"]}
data modify entity @e[tag=rlk_rd_hnew,limit=1] Rotation set from entity @s Rotation
data modify entity @e[tag=rlk_rd_hnew,limit=1] Rotation[1] set value 0f
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdShape $(shape)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdWind $(tell)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdDamage $(damage)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHLife $(life)
# World ticks newly spawned hazards in the creation frame: -1 -> 0.
scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHAge -1
scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHHit 0
scoreboard players set @e[tag=rlk_rd_hnew,limit=1] mlv 1
execute if entity @e[tag=rlk_raiden,limit=1] run scoreboard players operation @e[tag=rlk_rd_hnew,limit=1] mlv = @e[tag=rlk_raiden,limit=1] mlv
execute as @e[tag=rlk_rd_hnew,limit=1] at @s rotated as @s run function rlk:boss/raiden/hazard/init
tag @e[tag=rlk_rd_hnew] remove rlk_rd_hnew
