# The outward wheel turns back (@s = it): a new returning wheel here, flying back to her for as many ticks as the
# outward leg flew (she does not move while it flies), a new volley group. summon never takes the execute rotation (the
# new prop faces yaw 0), so the flight direction is aimed at her here: facing her feet, level.
execute store result storage rlk:kn core.wb.life int 1 run scoreboard players get @s mbPjT
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_b1","rlk_kn_wheel","rlk_kn_new"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 run function rlk:boss/arlecchino/p/b1/back with storage rlk:kn core.wb
