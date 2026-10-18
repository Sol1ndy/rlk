# [c_rocks] @s = the slab about to be thrown, at it: the dmg-0 throw line from its floor point toward the locked
# feet (rlk_mb_fg_p6tl), 1 b past them, w 2.4 (the blade reach), 10 t; the kit lane on it.
function rlk:mboss/mv/dist
scoreboard players add #mbDist mb 10
execute store result storage rlk:mboss fg.tl.len int 1 run scoreboard players get #mbDist mb
data modify storage rlk:mboss fg.tl merge value {w:24,tell:10,dmg:0,back:0,el:5,hold:3}
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 62
scoreboard players set #hzQuiet mb 1
execute positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p6tl,limit=1] feet rotated ~ 0 run function rlk:mboss/hz/line with storage rlk:mboss fg.tl
execute positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p6tl,limit=1] feet rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/line with storage rlk:mboss fg.tl
playsound minecraft:block.chain.hit hostile @a[tag=player] ~ ~ ~ 0.5 0.8 0.17
