# bomb clock 19
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 2
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] positioned ^1.2 ^ ^ positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:13,tell:10,dmg:80}
