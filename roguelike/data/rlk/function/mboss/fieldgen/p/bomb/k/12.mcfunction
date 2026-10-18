# bomb clock 12
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_fg_p1e,limit=1] run function rlk:mboss/mv/glide {t:45}
playsound minecraft:entity.breeze.charge hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
execute rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] positioned ^-1.2 ^ ^ run function rlk:mboss/fieldgen/p/bomb/drop
playsound minecraft:block.dispenser.launch hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 2
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] positioned ^1.2 ^ ^ positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:13,tell:10,dmg:80}
