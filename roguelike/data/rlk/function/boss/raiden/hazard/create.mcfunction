# Legacy preset (the release encounter): {shape:1..14, tell, damage, life}. Yaw is copied from @s as before.
execute unless score #rdKitV rd matches 2 run function rlk:boss/raiden/hazard/setup
summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_hazard","rlk_raiden_aux","rlk_room","rlk_rd_hnew"]}
data modify entity @e[tag=rlk_rd_hnew,limit=1] Rotation set from entity @s Rotation
data modify entity @e[tag=rlk_rd_hnew,limit=1] Rotation[1] set value 0f
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdShape $(shape)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdWind $(tell)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdDamage $(damage)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHLife $(life)
$function rlk:boss/raiden/hazard/preset/s$(shape)
function rlk:boss/raiden/hazard/born
