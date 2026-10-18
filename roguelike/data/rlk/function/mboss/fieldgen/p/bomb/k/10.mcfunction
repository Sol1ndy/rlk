# bomb clock 10
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
execute at @s rotated as @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.2} ^ ^3.8 ^ 1 0.1 1 0 10 force @a[tag=player]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 2
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] positioned ^0 ^ ^ positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:13,tell:10,dmg:80}
