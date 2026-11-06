# F1 resume (@s = body): the flood decal again with the ticks left to the next hit.
data modify storage rlk:kn core.dec set value {r:260,t:0}
execute if score #pt kn matches 110..159 run scoreboard players set #t kn 160
execute if score #pt kn matches 166..195 run scoreboard players set #t kn 196
execute unless score #pt kn matches 110..159 unless score #pt kn matches 166..195 run return 0
scoreboard players operation #t kn -= #pt kn
execute store result storage rlk:kn core.dec.t int 1 run scoreboard players get #t kn
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/decal/flood with storage rlk:kn core.dec
