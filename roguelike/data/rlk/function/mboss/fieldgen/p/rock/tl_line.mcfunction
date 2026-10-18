# @s = the slab about to be thrown: the throw line from its floor point toward the locked feet (dmg 0, 10 t).
function rlk:mboss/mv/dist
execute store result storage rlk:mboss fg.tl.len int 1 run scoreboard players get #mbDist mb
data modify storage rlk:mboss fg.tl merge value {w:24,tell:10,dmg:0}
execute positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p6tl,limit=1] feet run function rlk:mboss/hz/line with storage rlk:mboss fg.tl
