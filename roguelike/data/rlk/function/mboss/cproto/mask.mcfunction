scoreboard players set #hzR0 mb 25
execute at @s positioned ~ 201 ~ run function rlk:mboss/hz/mask {tell:30,dmg:110}
execute at @s positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_hzsafe","rlk_mb_cproto_safe"]}
execute at @s positioned ~ 201 ~5 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_hzsafe","rlk_mb_cproto_safe"]}
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_cproto_safe,tag=!rlk_mb_cproto_sg] mbHzSG = #hzLast mb
tag @e[type=minecraft:marker,tag=rlk_mb_cproto_safe] add rlk_mb_cproto_sg
