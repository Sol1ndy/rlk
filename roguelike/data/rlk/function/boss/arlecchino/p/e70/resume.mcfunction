# E70 resume (@s = body): the pool decal again with the ticks left to the brand.
execute unless score #pt kn matches 40..69 run return 0
scoreboard players set #t kn 70
scoreboard players operation #t kn -= #pt kn
data modify storage rlk:kn core.dec set value {r:120,t:0}
execute store result storage rlk:kn core.dec.t int 1 run scoreboard players get #t kn
execute at @s positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/decal/pool with storage rlk:kn core.dec
