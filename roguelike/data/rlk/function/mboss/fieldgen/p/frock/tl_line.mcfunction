# @s = the slab about to be thrown, at it: the throw line from its floor point to the locked feet (a quiet dmg-0
# hz/line w 2.4, tell 10, and the violet kit line with the same tell).
function rlk:mboss/mv/dist
execute store result storage rlk:mboss fg.f2l.len int 1 run scoreboard players get #mbDist mb
data modify storage rlk:mboss fg.f2l merge value {w:24,back:0,tell:10,el:9,hold:3,dmg:0}
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p12tl,limit=1] feet run function rlk:mboss/hz/line with storage rlk:mboss fg.f2l
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p12y
execute positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p12tl,limit=1] feet rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/line with storage rlk:mboss fg.f2l
playsound minecraft:block.chain.hit hostile @a[tag=player] ~ ~ ~ 0.5 0.8 0.17
